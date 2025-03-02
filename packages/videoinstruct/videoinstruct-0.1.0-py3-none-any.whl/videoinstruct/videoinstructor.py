import os
import datetime
from typing import Optional, Tuple
import json
import re
import shutil
from videoinstruct.agents.VideoInterpreter import VideoInterpreter
from videoinstruct.agents.DocGenerator import DocGenerator
from videoinstruct.agents.DocEvaluator import DocEvaluator
from videoinstruct.agents.ScreenshotAgent import ScreenshotAgent
from videoinstruct.utils.transcription import transcribe_video
from videoinstruct.utils.md2pdf import markdown_to_pdf, clean_markdown
from videoinstruct.configs import (
    ResponseType,
    DocGeneratorResponse,
    VideoInstructorConfig
)


class VideoInstructor:
    """
    A class that orchestrates the workflow between DocGenerator, VideoInterpreter, DocEvaluator, and ScreenshotAgent.
    
    This class handles:
    1. Video transcription extraction
    2. Passing transcription to DocGenerator
    3. Managing the Q&A flow between DocGenerator and VideoInterpreter
    4. Evaluating documentation quality with DocEvaluator
    5. Processing screenshots with ScreenshotAgent
    6. Collecting user feedback and refining documentation
    """
    
    def __init__(
        self,
        video_path: Optional[str] = None,
        transcription_path: Optional[str] = None,
        config: Optional[VideoInstructorConfig] = None
    ):
        """
        Initialize the VideoInstructor.
        
        Args:
            video_path: Path to the video file.
            transcription_path: Path to an existing transcription file (optional).
            config: Configuration for the VideoInstructor, including API keys and model settings.
        """
        self.video_path = video_path
        self.transcription_path = transcription_path
        self.transcription = None
        self.config = config or VideoInstructorConfig()
        
        # Create output and temp directories if they don't exist
        if not os.path.exists(self.config.output_dir):
            os.makedirs(self.config.output_dir)
        if not os.path.exists(self.config.temp_dir):
            os.makedirs(self.config.temp_dir)
        
        # Create a timestamped directory for this session
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = os.path.join(self.config.output_dir, self.timestamp)
        os.makedirs(self.session_dir, exist_ok=True)
        
        # Initialize DocGenerator with configuration
        self.doc_generator = DocGenerator(
            config=self.config.doc_generator_config,
            output_dir=self.session_dir
        )
        
        # Initialize VideoInterpreter with configuration
        self.video_interpreter = VideoInterpreter(
            config=self.config.video_interpreter_config
        )
        
        # Initialize DocEvaluator with configuration
        self.doc_evaluator = DocEvaluator(
            config=self.config.doc_evaluator_config
        )
        
        # Initialize ScreenshotAgent with configuration
        self.screenshot_agent = ScreenshotAgent(
            config=self.config.screenshot_agent_config,
            video_interpreter=self.video_interpreter,
            video_path=self.video_path,
            output_dir=self.session_dir
        )
        
        # Track document versions
        self.doc_version = 0
        
        # Load video and transcription if provided
        if video_path:
            self.load_video(video_path)
            
        if transcription_path:
            self.load_transcription(transcription_path)
    
    def load_video(self, video_path: str) -> None:
        """
        Load a video file and extract its transcription.
        
        Args:
            video_path: Path to the video file.
        """
        print(f"Loading video from {video_path}...")
        self.video_path = video_path
        
        # Update video path for ScreenshotAgent
        self.screenshot_agent.set_video_path(video_path)
        
        # Load video into VideoInterpreter
        self.video_interpreter.load_video(video_path)
        
        # Extract transcription if not already provided
        if not self.transcription:
            self._extract_transcription()
    
    def load_transcription(self, transcription_path: str) -> None:
        """
        Load an existing transcription file.
        
        Args:
            transcription_path: Path to the transcription file.
        """
        print(f"Loading transcription from {transcription_path}...")
        self.transcription_path = transcription_path
        
        try:
            with open(transcription_path, 'r') as file:
                self.transcription = file.read()
            
            # Set transcription in DocGenerator
            if self.transcription:
                self.doc_generator.set_transcription(self.transcription)
                print("Transcription loaded successfully.")
        except Exception as e:
            print(f"Error loading transcription: {str(e)}")
    
    def _extract_transcription(self) -> None:
        """Extract transcription from the loaded video."""
        if not self.video_path:
            raise ValueError("No video loaded. Please load a video first.")
        
        # Generate a default transcription path if not provided
        if not self.transcription_path:
            video_name = os.path.splitext(os.path.basename(self.video_path))[0]
            self.transcription_path = os.path.join(self.config.output_dir, f"{video_name}_transcription.txt")
        
        # Check if transcription file already exists
        if os.path.exists(self.transcription_path):
            print(f"Transcription file already exists at {self.transcription_path}. Loading existing transcription...")
            self.load_transcription(self.transcription_path)
            return
        
        print("Extracting transcription from video...")
        
        # Extract transcription using the utility function
        success = transcribe_video(
            video_path=self.video_path,
            output_path=self.transcription_path,
            temp_path=self.config.temp_dir
        )
        
        if success:
            # Load the transcription
            with open(self.transcription_path, 'r') as file:
                self.transcription = file.read()
            
            # Set transcription in DocGenerator
            self.doc_generator.set_transcription(self.transcription)
            print(f"Transcription extracted and saved to {self.transcription_path}")
        else:
            raise ValueError("Failed to extract transcription from video.")
    
    def _get_structured_response(self, response: str) -> DocGeneratorResponse:
        """
        Parse the response from DocGenerator to determine if it's a question or documentation.
        
        Args:
            response: The response from DocGenerator.
            
        Returns:
            A DocGeneratorResponse object with the type and content.
        """
        # Check if the response is in JSON format
        try:
            # Try to parse as JSON
            json_response = json.loads(response)
            if isinstance(json_response, dict) and "type" in json_response and "content" in json_response:
                # If the response has a type field, ensure it's one of our valid types
                if json_response["type"] not in [ResponseType.DOCUMENTATION, ResponseType.QUESTION]:
                    json_response["type"] = ResponseType.DOCUMENTATION
                return DocGeneratorResponse(**json_response)
        except json.JSONDecodeError:
            pass
        
        # If not JSON, use heuristics to determine if it's a question or documentation
        # Look for question patterns
        question_patterns = [
            r'\?\s*$',  # Ends with question mark
            r'^(?:can|could|what|when|where|which|who|why|how)',  # Starts with question word
            r'I need more information about',
            r'Please provide more details',
            r'Can you clarify',
        ]
        
        for pattern in question_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return DocGeneratorResponse(type=ResponseType.QUESTION, content=response)
        
        # If it contains markdown headers, it's likely documentation
        if re.search(r'^#\s+', response, re.MULTILINE):
            return DocGeneratorResponse(type=ResponseType.DOCUMENTATION, content=response)
        
        # Default to documentation
        return DocGeneratorResponse(type=ResponseType.DOCUMENTATION, content=response)
    
    def _save_documentation(self, documentation: str, is_final: bool = False) -> str:
        """
        Save the documentation to a file.
        
        Args:
            documentation: The documentation content to save.
            is_final: Whether this is the final version of the documentation.
            
        Returns:
            The path to the saved documentation file.
        """
        # Increment version number if not final
        if not is_final:
            self.doc_version += 1
            
        # Create a filename based on version number
        version_suffix = "_final" if is_final else f"_v{self.doc_version}"
        filename = f"documentation{version_suffix}.md"
        file_path = os.path.join(self.session_dir, filename)
        
        # Save the documentation to a file
        with open(file_path, 'w') as f:
            f.write(documentation)
        
        print(f"Documentation saved to {file_path}")
        
        # Process screenshots
        try:
            # Check if there are any screenshot placeholders in the documentation
            screenshot_pattern = r'\[SCREENSHOT_PLACEHOLDER\](.*?)\[/SCREENSHOT_PLACEHOLDER\]'
            screenshot_matches = list(re.finditer(screenshot_pattern, documentation, re.DOTALL))
            
            if not screenshot_matches:
                print("No screenshot placeholders found in the documentation.")
            else:
                print(f"Found {len(screenshot_matches)} screenshot placeholders in the documentation.")
            
            print("\n" + "="*50)
            print("PROCESSING SCREENSHOTS")
            print("="*50)
            
            # Verify that video_path and video_interpreter are set
            if not self.screenshot_agent.video_path:
                print("WARNING: No video path set for ScreenshotAgent. Screenshots cannot be processed.")
                raise ValueError("No video path set for ScreenshotAgent")
            
            if not self.screenshot_agent.video_interpreter:
                print("WARNING: No VideoInterpreter set for ScreenshotAgent. Screenshots cannot be processed.")
                raise ValueError("No VideoInterpreter set for ScreenshotAgent")
            
            # Process markdown file with screenshots
            enhanced_file_path = self.screenshot_agent.process_markdown_file(file_path)
            print("\n" + "="*50)
            print(f"Enhanced documentation with screenshots saved to {enhanced_file_path}")
            print("="*50)
            
            # Generate PDF from the enhanced markdown if configured to do so
            if os.path.exists(enhanced_file_path) and self.config.generate_pdf_for_all_versions:
                pdf_path = self._generate_pdf(enhanced_file_path)
                if pdf_path:
                    print(f"PDF successfully generated at: {pdf_path}")
                else:
                    print("Failed to generate PDF from enhanced markdown.")
            elif not self.config.generate_pdf_for_all_versions:
                print("Skipping PDF generation as per configuration.")
            else:
                print(f"Warning: Enhanced markdown file not found at {enhanced_file_path}")
            
            return enhanced_file_path
        except Exception as e:
            print(f"Error processing screenshots: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # If screenshot processing fails, still return the original file path
            
            # Generate PDF from the original markdown if configured to do so
            if self.config.generate_pdf_for_all_versions:
                pdf_path = self._generate_pdf(file_path)
                if pdf_path:
                    print(f"PDF successfully generated from original markdown at: {pdf_path}")
                else:
                    print("Failed to generate PDF from original markdown.")
            else:
                print("Skipping PDF generation as per configuration.")
            
            return file_path
    
    def _generate_pdf(self, markdown_path: str) -> str:
        """
        Generate a PDF from a Markdown file using the md2pdf utility.
        
        Args:
            markdown_path: Path to the Markdown file
            
        Returns:
            Path to the generated PDF file, or None if generation failed
        """
        try:
            print(f"Generating PDF from markdown: {markdown_path}")
            
            if not os.path.exists(markdown_path):
                print(f"Error: Markdown file not found at {markdown_path}")
                return None
                
            # Read the markdown content
            with open(markdown_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
            
            # Clean the Markdown text using the utility function
            cleaned_md_text = clean_markdown(md_text)
            
            # Create a temporary markdown file with the cleaned content
            temp_md_path = f"{os.path.splitext(markdown_path)[0]}_enhanced.md"
            with open(temp_md_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_md_text)
            
            # Define the output PDF path
            pdf_path = f"{os.path.splitext(markdown_path)[0]}.pdf"
            
            # Determine the base directory from the Markdown file's absolute path
            base_path = os.path.dirname(os.path.abspath(markdown_path))
            
            # Generate the PDF with images resolved relative to the Markdown file's directory
            markdown_to_pdf(cleaned_md_text, pdf_path, base_path)
            
            # Verify the PDF was created
            if os.path.exists(pdf_path):
                print(f"PDF generated successfully: {pdf_path}")
                
                # Clean up temporary file
                if os.path.exists(temp_md_path):
                    os.remove(temp_md_path)
                    
                return pdf_path
            else:
                print("PDF generation failed: Output file not found")
                return None
                
        except Exception as e:
            print(f"Error in _generate_pdf: {str(e)}")
            return None
    
    def _evaluate_documentation(self, documentation: str, print_documentation: bool = True) -> Tuple[bool, str]:
        """
        Evaluate the documentation using the DocEvaluator.
        
        Args:
            documentation: The documentation to evaluate.
            print_documentation: Whether to print the documentation to the console.
            
        Returns:
            A tuple of (is_approved, feedback)
        """
        # Show the documentation to the user before evaluation if requested
        if print_documentation:
            print("\n" + "="*50)
            print("GENERATED DOCUMENTATION:")
            print("="*50)
            print(documentation)
            print("\n" + "="*50)
        
        print("EVALUATING DOCUMENTATION...")
        
        # Find the enhanced markdown file path based on the current version
        enhanced_md_path = os.path.join(self.session_dir, f"documentation_v{self.doc_version}_enhanced.md")
        
        # Check if enhanced markdown exists
        if os.path.exists(enhanced_md_path):
            try:
                # Read the enhanced markdown content
                with open(enhanced_md_path, 'r', encoding='utf-8') as f:
                    enhanced_documentation = f.read()
                
                print(f"Using enhanced markdown for evaluation: {enhanced_md_path}")
                # Evaluate with enhanced markdown
                is_approved, feedback = self.doc_evaluator.evaluate_documentation(enhanced_documentation)
            except Exception as e:
                print(f"Error evaluating with enhanced markdown: {str(e)}")
                # Fall back to text-only evaluation with original documentation
                is_approved, feedback = self.doc_evaluator.evaluate_documentation(documentation)
        else:
            # Fall back to text-only evaluation with original documentation
            is_approved, feedback = self.doc_evaluator.evaluate_documentation(documentation)
        
        if is_approved:
            print("Documentation APPROVED by DocEvaluator")
            print(f"Feedback: {feedback}")
        else:
            print("Documentation REJECTED by DocEvaluator")
            print(f"Feedback: {feedback}")
            
            # Print the number of rejections so far
            print(f"Rejection count: {self.doc_evaluator.rejection_count}/{self.doc_evaluator.config.max_rejection_count}")
            
            if self.doc_evaluator.should_escalate_to_user():
                print("Maximum rejections reached. Will escalate to user.")
        
        return is_approved, feedback
    
    def _get_user_feedback(self, documentation: str) -> Tuple[str, bool]:
        """
        Get feedback from the user about the documentation.
        
        Args:
            documentation: The documentation to get feedback on.
            
        Returns:
            A tuple of (feedback, is_satisfied)
        """
        # Show the most recent feedback if available
        most_recent_feedback = ""
        if self.doc_evaluator.feedback_history and len(self.doc_evaluator.feedback_history) > 0:
            most_recent_feedback = self.doc_evaluator.feedback_history[-1]
            print("\nMost recent evaluator feedback:")
            print(most_recent_feedback)
        
        # Find the enhanced markdown file path
        enhanced_md_path = os.path.join(self.session_dir, f"documentation_v{self.doc_version}_enhanced.md")
        
        # Check if enhanced markdown exists and inform the user
        if os.path.exists(enhanced_md_path):
            print(f"\nAn enhanced version of the documentation is available at: {enhanced_md_path}")
            print("For the best viewing experience with images, please open this file.")
        
        # Check if PDF exists and inform the user
        pdf_path = os.path.join(self.session_dir, f"documentation_v{self.doc_version}.pdf")
        
        # If the enhanced markdown exists but the PDF doesn't, generate it
        if os.path.exists(enhanced_md_path) and not os.path.exists(pdf_path) and self.config.generate_pdf_for_all_versions:
            print("Generating PDF from enhanced markdown...")
            pdf_path = self._generate_pdf(enhanced_md_path)
            if pdf_path:
                print(f"PDF successfully generated at: {pdf_path}")
            else:
                print("Failed to generate PDF from enhanced markdown.")
        
        if os.path.exists(pdf_path):
            print(f"\nA PDF version of the documentation is also available at: {pdf_path}")
        
        while True:
            user_input = input("\nAre you satisfied with this documentation? (yes/no): ").strip().lower()
            if user_input in ['yes', 'y']:
                # Rename the last version of the documentation with _final suffix
                try:
                    # Get the source files (both markdown and PDF if available)
                    md_source = os.path.join(self.session_dir, f"documentation_v{self.doc_version}.md")
                    enhanced_md_source = os.path.join(self.session_dir, f"documentation_v{self.doc_version}_enhanced.md")
                    pdf_source = os.path.join(self.session_dir, f"documentation_v{self.doc_version}.pdf")
                    
                    # Create the destination paths with _final suffix
                    md_dest = os.path.join(self.session_dir, f"documentation_final.md")
                    enhanced_md_dest = os.path.join(self.session_dir, f"documentation_final_enhanced.md")
                    pdf_dest = os.path.join(self.session_dir, f"documentation_final.pdf")
                    
                    # Rename the markdown file
                    if os.path.exists(md_source):
                        shutil.copy2(md_source, md_dest)
                        print(f"Final documentation saved as: {md_dest}")
                    
                    # Rename the enhanced markdown file if it exists
                    if os.path.exists(enhanced_md_source):
                        shutil.copy2(enhanced_md_source, enhanced_md_dest)
                        print(f"Final enhanced documentation saved as: {enhanced_md_dest}")
                        
                        # Generate PDF from the final enhanced markdown if it doesn't exist
                        if not os.path.exists(pdf_dest) and not os.path.exists(pdf_source) and self.config.generate_pdf_for_all_versions:
                            pdf_path = self._generate_pdf(enhanced_md_dest)
                            if pdf_path:
                                print(f"Final PDF documentation generated at: {pdf_path}")
                    
                    # Copy the PDF file if it exists
                    if os.path.exists(pdf_source):
                        shutil.copy2(pdf_source, pdf_dest)
                        print(f"Final PDF documentation saved as: {pdf_dest}")
                except Exception as e:
                    print(f"Warning: Could not create final documentation copies: {str(e)}")
                return "", True
            elif user_input in ['no', 'n']:
                feedback = input("Please provide feedback to improve the documentation (press Enter to use evaluator's feedback): ")
                # If user just presses Enter, use the most recent feedback from the evaluator
                if not feedback.strip() and most_recent_feedback:
                    print(f"Using evaluator's feedback: {most_recent_feedback}")
                    return most_recent_feedback, False
                return feedback, False
            else:
                print("Please answer 'yes' or 'no'.")
    
    def _handle_user_question(self, question: str) -> str:
        """
        Let the user answer a question instead of the VideoInterpreter.
        
        Args:
            question: The question to ask the user.
            
        Returns:
            The user's answer.
        """
        print("\n" + "="*50)
        print("QUESTION FROM DOC GENERATOR:")
        print("="*50)
        print(question)
        print("\n" + "="*50)
        
        user_answer = input("\nPlease answer this question (or type 'interpreter' to let the VideoInterpreter answer): ")
        
        if user_answer.strip().lower() == 'interpreter':
            print("Asking VideoInterpreter instead...")
            return self.video_interpreter.respond(question)
        
        return user_answer
    
    def _prepare_initial_prompt(self) -> str:
        """
        Prepare the initial prompt for documentation generation by combining
        the transcription and a detailed description from the VideoInterpreter.
        
        Returns:
            A formatted initial prompt string for the DocGenerator.
        """
        # First, get a detailed step-by-step description from the VideoInterpreter
        print("Getting initial step-by-step description from VideoInterpreter...")
        initial_description = self.video_interpreter.respond(
            "Please provide a detailed step-by-step description of what is happening in this video. "
            "Focus on the actions being performed, the sequence of steps, and any important visual details. "
            "Be as specific and comprehensive as possible."
        )
        print("Initial description received from VideoInterpreter.")
        
        # Prepare the initial prompt with transcription and description
        print("Preparing DocGenerator with transcription and initial description...")
        initial_prompt = f"""
        You will be creating a step-by-step guide based on a video.
        
        Here is the transcription of the video:
        
        TRANSCRIPTION:
        {self.transcription}
        
        Additionally, here is a detailed description of what happens in the video:
        
        VIDEO DESCRIPTION:
        {initial_description}
        
        Using both the transcription and the video description, create a comprehensive step-by-step guide.
        If you have any questions or need clarification about specific parts of the video, please ask.
        """
        
        return initial_prompt
    
    def generate_documentation(self) -> str:
        """
        Generate step-by-step documentation from the loaded video.
        
        Returns:
            The generated documentation as a string.
        """
        if not self.transcription:
            raise ValueError("No transcription available. Please load a video or transcription first.")
        
        print("Starting documentation generation workflow...")
        
        # Reset DocEvaluator memory at the start of a new documentation generation
        self.doc_evaluator.reset_memory()
        
        # Reset document version counter
        self.doc_version = 0
        
        # Prepare the initial prompt
        initial_prompt = self._prepare_initial_prompt()
        
        # Initialize counters
        iteration_count = 0
        question_count = 0
        current_documentation = None
        is_satisfied = False
        
        # Start the documentation generation process
        response = self.doc_generator.generate_documentation_with_description(initial_prompt)
        structured_response = self._get_structured_response(response)
        
        while iteration_count < self.config.max_iterations and not is_satisfied:
            iteration_count += 1
            
            if structured_response.type == ResponseType.QUESTION:
                question_count += 1
                question = structured_response.content
                
                # Check if we should ask the user instead of the VideoInterpreter
                if question_count % self.config.user_feedback_interval == 0:
                    answer = self._handle_user_question(question)
                else:
                    print(f"\nQuestion from DocGenerator ({question_count}):")
                    print(question)
                    answer = self.video_interpreter.respond(question)
                    print(f"Answer from VideoInterpreter:")
                    print(answer)
                
                # Send the answer back to DocGenerator
                response = self.doc_generator.refine_documentation(f"ANSWER: {answer}")
                structured_response = self._get_structured_response(response)
            
            elif structured_response.type == ResponseType.DOCUMENTATION:
                current_documentation = structured_response.content
                
                # Save the current version of the documentation
                self._save_documentation(current_documentation)
                
                # Print the documentation when it's first generated or refined
                print("\n" + "="*50)
                print("GENERATED DOCUMENTATION:")
                print("="*50)
                print(current_documentation)
                print("\n" + "="*50)
                
                # First, let the DocEvaluator evaluate the documentation
                evaluation_count = self.doc_evaluator.rejection_count + 1
                print(f"\nEvaluation round #{evaluation_count}")
                
                # Don't print the documentation during evaluation since we just printed it
                is_approved, feedback = self._evaluate_documentation(current_documentation, print_documentation=False)
                
                print(f"Evaluator's feedback: {feedback}")

                # Check if we should escalate to user due to repeated rejections
                if not is_approved and self.doc_evaluator.should_escalate_to_user():
                    print("\n" + "="*50)
                    print("ESCALATING TO USER: DocEvaluator has rejected the documentation multiple times.")
                    print("="*50)
                    user_feedback, is_satisfied = self._get_user_feedback(current_documentation)
                    
                    # Reset the rejection count after user intervention
                    self.doc_evaluator.reset_rejection_count()
                    
                    if not is_satisfied and user_feedback:
                        # Refine documentation based on user feedback
                        response = self.doc_generator.refine_documentation(user_feedback)
                        structured_response = self._get_structured_response(response)
                    elif is_satisfied:
                        # User is satisfied, break the loop
                        break
                
                # If DocEvaluator approved or we're continuing after rejection
                elif is_approved:
                    # DocEvaluator approved, now get user feedback
                    user_feedback, is_satisfied = self._get_user_feedback(current_documentation)
                    
                    if not is_satisfied and user_feedback:
                        # Refine documentation based on user feedback
                        response = self.doc_generator.refine_documentation(user_feedback)
                        structured_response = self._get_structured_response(response)
                    elif is_satisfied:
                        # User is satisfied, break the loop
                        break
                else:
                    # DocEvaluator rejected but not enough times to escalate to user
                    # Refine documentation based on DocEvaluator feedback
                    response = self.doc_generator.refine_documentation(f"FEEDBACK: {feedback}")
                    structured_response = self._get_structured_response(response)
                
                # Check if we should get user feedback based on iteration count
                if not is_approved and iteration_count % self.config.user_feedback_interval == 0:
                    user_feedback, is_satisfied = self._get_user_feedback(current_documentation)
                    
                    if not is_satisfied and user_feedback:
                        # Refine documentation based on user feedback
                        response = self.doc_generator.refine_documentation(user_feedback)
                        structured_response = self._get_structured_response(response)
                    elif is_satisfied:
                        # User is satisfied, break the loop
                        break
        
        # Return the final documentation
        if current_documentation:
            print(f"\nFinal documentation saved in: {self.session_dir}")
            return current_documentation
        else:
            print("No documentation was generated.")
            return ""