import os
import re
from typing import List, Optional, Dict, Tuple
import litellm

from videoinstruct.configs import DocEvaluatorConfig
from videoinstruct.prompt_loader import DOC_EVALUATOR_SYSTEM_PROMPT

class DocEvaluator:
    """
    A class for evaluating the quality of documentation using LLMs.
    
    This class handles:
    1. Evaluating documentation against quality criteria
    2. Providing feedback for improvement
    3. Tracking evaluation history
    4. Determining when to escalate to human review
    """
    
    def __init__(
        self,
        config: Optional[DocEvaluatorConfig] = None
    ):
        """
        Initialize the DocEvaluator.
        
        Args:
            config: Configuration for the LLM model, including model provider and API key.
        """
        self.config = config or DocEvaluatorConfig()
        self.model_provider = self.config.model_provider
        self.rejection_count = 0
        self.conversation_history = []  # Store the full conversation history
        self.feedback_history = []  # Store just the feedback for easy access
        
        # Initialize conversation with system message
        self.conversation_history = [
            {"role": "system", "content": self.config.system_instruction}
        ]
        
        # Set API key from config if provided
        if self.config.api_key:
            if self.model_provider == "deepseek":
                os.environ["DEEPSEEK_API_KEY"] = self.config.api_key
            elif self.model_provider == "openai":
                os.environ["OPENAI_API_KEY"] = self.config.api_key
            elif self.model_provider == "anthropic":
                os.environ["ANTHROPIC_API_KEY"] = self.config.api_key
            # Add other providers as needed
    
    def evaluate_documentation(self, documentation: str) -> Tuple[bool, str]:
        """
        Evaluate the quality of the provided documentation.
        
        Args:
            documentation: The documentation to evaluate in markdown format.
            
        Returns:
            A tuple of (is_approved, feedback)
        """
        # Prepare the prompt for evaluation
        if len(self.conversation_history) == 1:  # Only system message exists
            # First evaluation
            evaluation_prompt = f"""
            Please evaluate the following documentation for quality, clarity, and completeness:
            
            ```markdown
            {documentation}
            ```
            
            Provide your evaluation according to the criteria in your instructions.
            """
        else:
            # Subsequent evaluation (revision)
            evaluation_prompt = f"""
            I've revised the documentation based on your feedback. Please evaluate this updated version:
            
            ```markdown
            {documentation}
            ```
            
            Has it improved? Are there still issues that need to be addressed?
            """
        
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": evaluation_prompt})
        
        # Get response from LLM using the full conversation history
        response = self._get_llm_response(self.conversation_history)
        
        # Add assistant response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Extract Python code from the response using regex
        python_code_match = re.search(r'```python\s*({.*?})\s*```', response, re.DOTALL)
        
        if python_code_match:
            # Extract the Python dictionary code
            python_code = python_code_match.group(1).strip()
            
            try:
                # Safely evaluate the Python code
                result = eval(python_code)
                
                # Check if the result is a dictionary with the expected keys
                if isinstance(result, dict) and "approved" in result and "feedback" in result:
                    is_approved = bool(result["approved"])
                    feedback = str(result["feedback"])
                    
                    # Store feedback in history if it's a rejection
                    if not is_approved:
                        self.feedback_history.append(feedback)
                        self.rejection_count += 1
                    else:
                        self.rejection_count = 0
                    
                    return is_approved, feedback
            except Exception as e:
                print(f"Error evaluating Python code: {str(e)}")
        
        # Fallback: Use heuristics to determine approval
        is_approved = "approved" in response.lower() and not any(x in response.lower() for x in ["reject", "not approved", "disapproved"])
        
        # Extract feedback using regex if possible
        feedback_match = re.search(r'feedback["\']:\s*["\'](.+?)["\']', response, re.DOTALL | re.IGNORECASE)
        if feedback_match:
            feedback = feedback_match.group(1)
        else:
            feedback = response
        
        # Store feedback in history if it's a rejection
        if not is_approved:
            self.feedback_history.append(feedback)
            self.rejection_count += 1
        else:
            self.rejection_count = 0
        
        return is_approved, feedback
    
    def evaluate_documentation_with_pdf(self, documentation: str, pdf_path: str) -> Tuple[bool, str]:
        """
        Evaluate the quality of the provided documentation with PDF.
        This method is kept for backward compatibility but now uses text-based evaluation.
        
        Args:
            documentation: The documentation content as text.
            pdf_path: Path to the PDF file (not used).
            
        Returns:
            A tuple of (is_approved, feedback)
        """
        print(f"PDF available at {pdf_path}, but using text-based evaluation as per configuration")
        return self.evaluate_documentation(documentation)
    
    def should_escalate_to_user(self) -> bool:
        """
        Determine if the evaluation should be escalated to a human user.
        
        Returns:
            True if the number of rejections exceeds the configured maximum.
        """
        return self.rejection_count >= self.config.max_rejection_count
    
    def reset_rejection_count(self) -> None:
        """Reset the rejection count."""
        self.rejection_count = 0
    
    def reset_memory(self) -> None:
        """Reset the conversation history, feedback history, and rejection count."""
        self.conversation_history = [
            {"role": "system", "content": self.config.system_instruction}
        ]
        self.feedback_history = []
        self.rejection_count = 0
    
    def get_feedback_history(self) -> List[str]:
        """
        Get the history of feedback provided.
        
        Returns:
            A list of feedback strings in chronological order.
        """
        return self.feedback_history
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the full conversation history.
        
        Returns:
            A list of message dictionaries with 'role' and 'content' keys.
        """
        return self.conversation_history
    
    def _get_llm_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Get a response from the LLM.
        
        Args:
            messages: The conversation messages.
            
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
        if model_name == "anthropic/claude-3-7-sonnet-latest":
            generate_config["thinking"] = {"type": "enabled", "budget_tokens": 1024}
            generate_config["temperature"] = 1
        
        # Remove response_format since we're not using JSON anymore
        generate_config["drop_params"] = True
        
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
            # If there's reasoning content available (for DeepSeek Reasoner)
            try:
                return response.choices[0].message.reasoning_content
            except:
                return f"Error: {str(e)}"


# Example usage:
# doc_evaluator = DocEvaluator(
#     config=DocEvaluatorConfig(
#         api_key=os.getenv("DEEPSEEK_API_KEY"),
#         model_provider="deepseek",
#         model="deepseek-reasoner"
#     )
# )
# is_approved, feedback = doc_evaluator.evaluate_documentation("# Sample Documentation\n\nThis is a test.")
# print(f"Approved: {is_approved}\nFeedback: {feedback}")
#
# # Later, evaluate a revised version
# is_approved, feedback = doc_evaluator.evaluate_documentation("# Sample Documentation\n\nThis is a revised test with more details.")
# print(f"Approved: {is_approved}\nFeedback: {feedback}") 