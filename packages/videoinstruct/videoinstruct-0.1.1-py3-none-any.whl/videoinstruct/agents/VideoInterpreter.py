from google import genai
from google.genai import types
import time
import os
from typing import Optional
from IPython.display import Markdown

from videoinstruct.configs import VideoInterpreterConfig


class VideoInterpreter:
    """A class for interpreting videos using Google's Gemini API."""
    
    def __init__(
        self,
        config: Optional[VideoInterpreterConfig] = None,
        video_path: Optional[str] = None
    ):
        """
        Initialize the VideoInterpreter.
        
        Args:
            config: Configuration for the Gemini model, including API key.
            video_path: Path to the video file to interpret.
        """
        self.config = config or VideoInterpreterConfig()
        
        # Get API key from config or environment variable
        self.api_key = self.config.api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided in config or set as GEMINI_API_KEY environment variable")
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)
        
        self.video_file = None
        self.conversation_history = []
        
        # Load video if provided
        if video_path:
            self.load_video(video_path)
    
    def load_video(self, video_path: str) -> None:
        """
        Load a video file for interpretation.
        
        Args:
            video_path: Path to the video file.
        """
        self.video_file = self.client.files.upload(file=video_path)
        
        # Check whether the file is ready to be used
        while self.video_file.state.name == "PROCESSING":
            print('.', end='')
            time.sleep(1)
            self.video_file = self.client.files.get(name=self.video_file.name)
        
        if self.video_file.state.name == "FAILED":
            raise ValueError(f"Video processing failed: {self.video_file.state.name}")
        
        print('Video loaded successfully')
        # Reset conversation history when loading a new video
        self.conversation_history = []
    
    def respond(self, question: str) -> str:
        """
        Respond to a question about the loaded video.
        
        Args:
            question: The question to ask about the video.
            
        Returns:
            The model's response as text.
        """
        if not self.video_file:
            raise ValueError("No video loaded. Please load a video first using load_video().")
        
        # Add user question to conversation history
        self.conversation_history.append(f"user: {question}")
        
        # Prepare contents for the API call
        contents = [self.video_file]
        if self.conversation_history:
            contents.append(", ".join(self.conversation_history))
        
        # Prepare configuration
        generate_config = {}
        if self.config.system_instruction:
            generate_config["system_instruction"] = self.config.system_instruction
        if self.config.max_output_tokens:
            generate_config["max_output_tokens"] = self.config.max_output_tokens
        if self.config.top_k:
            generate_config["top_k"] = self.config.top_k
        if self.config.top_p:
            generate_config["top_p"] = self.config.top_p
        if self.config.temperature:
            generate_config["temperature"] = self.config.temperature
        if self.config.response_mime_type:
            generate_config["response_mime_type"] = self.config.response_mime_type
        if self.config.stop_sequences:
            generate_config["stop_sequences"] = self.config.stop_sequences
        if self.config.seed:
            generate_config["seed"] = self.config.seed
        
        # Generate response
        response = self.client.models.generate_content(
            contents=contents,
            model=self.config.model,
            config=types.GenerateContentConfig(**generate_config),
        )
        
        # Add assistant response to conversation history
        self.conversation_history.append(f"assistant: {response.text}")
        
        return response.text
    
    def remove_memory(self) -> None:
        """Reset the conversation history while keeping the video loaded."""
        self.conversation_history = []
        print("Conversation history has been reset.")
    
    def delete_video(self) -> None:
        """Delete the loaded video and reset the conversation history."""
        if not self.video_file:
            print("No video is currently loaded.")
            return
        
        try:
            # Delete the video file
            self.client.files.delete(name=self.video_file.name)
            print(f"Video {self.video_file.name} has been deleted.")
            
            # Reset video file and conversation history
            self.video_file = None
            self.conversation_history = []
        except genai.errors.ClientError as e:
            print(f"Error deleting video: {e.message}")
    
    def display_response(self, response_text: str) -> None:
        """
        Display the response as Markdown (useful in Jupyter notebooks).
        
        Args:
            response_text: The text to display as Markdown.
        """
        return Markdown(response_text)


# Example usage:
# interpreter = VideoInterpreter()
# interpreter.load_video("test_video.mp4")
# response = interpreter.respond("Summarize the video in 100 words.")
# interpreter.display_response(response)