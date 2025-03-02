import os
import time
from typing import List, Optional, Dict
import json
import litellm
from IPython.display import Markdown
import re

from videoinstruct.configs import DocGeneratorConfig
from videoinstruct.prompt_loader import DOC_GENERATOR_SYSTEM_PROMPT


class DocGenerator:
    """
    A class for generating documentation from video transcriptions using LLMs.
    
    This class handles:
    1. Processing video transcriptions
    2. Generating step-by-step documentation
    3. Refining documentation based on feedback
    4. Saving and displaying the generated documentation
    """
    
    def __init__(
        self,
        config: Optional[DocGeneratorConfig] = None,
        transcription: Optional[str] = None,
        output_dir: str = "output"
    ):
        """
        Initialize the DocGenerator.
        
        Args:
            config: Configuration for the LLM model, including model provider and API key.
            transcription: The transcription of the video to generate documentation for.
            output_dir: Directory to save the generated documentation.
        """
        self.config = config or DocGeneratorConfig()
        self.model_provider = self.config.model_provider
        self.transcription = transcription
        self.conversation_history = []
        self.output_dir = output_dir
        
        # Set API key from config if provided
        if self.config.api_key:
            if self.model_provider == "openai":
                os.environ["OPENAI_API_KEY"] = self.config.api_key
            elif self.model_provider == "anthropic":
                os.environ["ANTHROPIC_API_KEY"] = self.config.api_key
            elif self.model_provider == "deepseek":
                os.environ["DEEPSEEK_API_KEY"] = self.config.api_key
            # Add other providers as needed
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def set_transcription(self, transcription: str) -> None:
        """
        Set the video transcription.
        
        Args:
            transcription: The transcription of the video.
        """
        self.transcription = transcription
        # Reset conversation history when setting a new transcription
        self.conversation_history = []
    
    def generate_documentation(self) -> str:
        """
        Generate step-by-step documentation based on the video transcription.
        
        Returns:
            The generated documentation in markdown format or a structured JSON response.
        """
        if not self.transcription:
            raise ValueError("No transcription provided. Please set a transcription first.")
        
        # Initial prompt to generate documentation
        initial_prompt = f"""
        Based on the following video transcription, create a step-by-step guide:
        
        TRANSCRIPTION:
        {self.transcription}
        
        Generate a detailed markdown guide that explains how to perform the task shown in the video.
        If you have any questions or need clarification about specific parts of the video, please ask.
        """
        
        # Add initial prompt to conversation history
        self.conversation_history.append({"role": "user", "content": initial_prompt})
        
        # Generate response
        response = self._get_llm_response(self.conversation_history)
        
        # Add assistant response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def generate_documentation_with_description(self, initial_prompt: str) -> str:
        """
        Generate step-by-step documentation based on both video transcription and a detailed description.
        
        Args:
            initial_prompt: A prompt containing both the transcription and a detailed description
                           of the video from the VideoInterpreter.
                           
        Returns:
            The generated documentation in markdown format or a structured JSON response.
        """
        # Add initial prompt to conversation history
        self.conversation_history.append({"role": "user", "content": initial_prompt})
        
        # Generate response
        response = self._get_llm_response(self.conversation_history)
        
        # Add assistant response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def refine_documentation(self, feedback: str) -> str:
        """
        Refine the documentation based on feedback or additional information.
        
        Args:
            feedback: Feedback or additional information to improve the documentation.
            
        Returns:
            The refined documentation in markdown format or a structured JSON response.
        """
        if not self.conversation_history:
            raise ValueError("No documentation has been generated yet.")
        
        # Add feedback to conversation history
        self.conversation_history.append({"role": "user", "content": feedback})
        
        # Generate response
        response = self._get_llm_response(self.conversation_history)
        
        # Add assistant response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _get_llm_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Get a response from the LLM.
        
        Args:
            messages: The conversation history.
            
        Returns:
            The LLM's response as text.
        """
        # Prepare model name based on provider
        model_name = self.config.model
        if self.model_provider != "openai" and not "/" in model_name:
            model_name = f"{self.model_provider}/{model_name}"
        
        # Prepare configuration for the API call
        generate_config = {}
        if self.config.max_output_tokens:
            generate_config["max_tokens"] = self.config.max_output_tokens
        if self.config.temperature:
            generate_config["temperature"] = self.config.temperature
        if self.config.top_p:
            generate_config["top_p"] = self.config.top_p
        if self.config.stream:
            generate_config["stream"] = self.config.stream
        if self.config.seed:
            generate_config["seed"] = self.config.seed
        if self.config.response_format:
            generate_config["response_format"] = self.config.response_format
        
        # Ensure drop_params is set to true
        generate_config["drop_params"] = True

        # Add system instruction if provided
        if self.config.system_instruction:
            system_message = {"role": "system", "content": self.config.system_instruction}
            messages = [system_message] + messages
        
        try:
            # Generate response using litellm
            response = litellm.completion(
                model=model_name,
                messages=messages,
                **generate_config
            )
            
            # Extract text from response
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"
    
    def save_documentation(self, filename: str = None) -> str:
        """
        Save the generated documentation to a markdown file.
        
        Args:
            filename: The name of the file to save the documentation to.
                     If None, a default name will be generated.
                     
        Returns:
            The path to the saved file.
        """
        if not self.conversation_history:
            raise ValueError("No documentation has been generated yet.")
        
        # Get the latest documentation
        latest_doc = None
        for message in reversed(self.conversation_history):
            if message["role"] == "assistant":
                content = message["content"]
                # Try to parse as JSON
                try:
                    json_content = json.loads(content)
                    if isinstance(json_content, dict) and "content" in json_content:
                        if json_content.get("type") in ["documentation", "complete"]:
                            latest_doc = json_content["content"]
                            break
                except json.JSONDecodeError:
                    # If not JSON, check if it's not a question
                    if not content.strip().endswith("?") and not content.startswith("VIDEO RESPONSE:"):
                        latest_doc = content
                        break
        
        if not latest_doc:
            raise ValueError("No documentation found in conversation history.")
        
        # Generate filename if not provided
        if not filename:
            # Extract title from markdown
            title_match = re.search(r'^#\s+(.+)$', latest_doc, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
                # Convert title to filename-friendly format
                filename = re.sub(r'[^\w\s-]', '', title).strip().lower()
                filename = re.sub(r'[-\s]+', '-', filename)
            else:
                # Use timestamp if no title found
                filename = f"documentation-{int(time.time())}"
        
        # Ensure filename has .md extension
        if not filename.endswith('.md'):
            filename += '.md'
        
        # Full path to save the file
        file_path = os.path.join(self.output_dir, filename)
        
        # Save documentation to file
        with open(file_path, 'w') as f:
            f.write(latest_doc)
        
        print(f"Documentation saved to {file_path}")
        return file_path
    
    def display_documentation(self) -> None:
        """
        Display the latest documentation as Markdown (useful in Jupyter notebooks).
        """
        if not self.conversation_history:
            raise ValueError("No documentation has been generated yet.")
        
        # Get the latest documentation
        latest_doc = None
        for message in reversed(self.conversation_history):
            if message["role"] == "assistant":
                content = message["content"]
                # Try to parse as JSON
                try:
                    json_content = json.loads(content)
                    if isinstance(json_content, dict) and "content" in json_content:
                        if json_content.get("type") in ["documentation", "complete"]:
                            latest_doc = json_content["content"]
                            break
                except json.JSONDecodeError:
                    # If not JSON, check if it's not a question
                    if not content.strip().endswith("?") and not content.startswith("VIDEO RESPONSE:"):
                        latest_doc = content
                        break
        
        if not latest_doc:
            raise ValueError("No documentation found in conversation history.")
        
        return Markdown(latest_doc)
    
    def _extract_questions(self, text: str) -> List[str]:
        """
        Extract questions from text.
        
        Args:
            text: Text containing questions.
            
        Returns:
            List of extracted questions.
        """
        # Simple pattern matching for questions
        questions = re.findall(r'(?:^|\n)\s*\d+\.\s*([^\n]+\?)', text)
        
        # If numbered list not found, try to find sentences ending with question marks
        if not questions:
            questions = re.findall(r'([^.!?\n]+\?)', text)
        
        return questions


# Example usage:
# doc_generator = DocGenerator(
#     config=DocGeneratorConfig(
#         api_key=os.getenv("OPENAI_API_KEY"),
#         model_provider="openai",
#         model="gpt-4o"
#     )
# )
# doc_generator.set_transcription("This is a transcription of a video showing how to create a new GitHub repository...")
# documentation = doc_generator.generate_documentation()
# print(documentation)
