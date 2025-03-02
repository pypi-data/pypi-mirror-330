#!/usr/bin/env python
import argparse
import os
import sys
from pathlib import Path

from videoinstruct.videoinstructor import VideoInstructor, VideoInstructorConfig
from videoinstruct.agents.DocGenerator import DocGeneratorConfig
from videoinstruct.agents.VideoInterpreter import VideoInterpreterConfig
from videoinstruct.agents.DocEvaluator import DocEvaluatorConfig


def main():
    parser = argparse.ArgumentParser(
        description="VideoInstruct: Generate documentation from instructional videos"
    )
    parser.add_argument(
        "video_path", type=str, help="Path to the video file to process"
    )
    parser.add_argument(
        "--output-dir", type=str, default="output", help="Directory to save output files"
    )
    parser.add_argument(
        "--temp-dir", type=str, default="temp", help="Directory for temporary files"
    )
    parser.add_argument(
        "--max-iterations", type=int, default=15, help="Maximum number of refinement iterations"
    )
    parser.add_argument(
        "--user-feedback-interval", type=int, default=3, help="Get user feedback every N iterations"
    )
    parser.add_argument(
        "--doc-generator-model", type=str, default="gpt-4o-mini", help="Model for DocGenerator"
    )
    parser.add_argument(
        "--video-interpreter-model", type=str, default="gemini-2.0-flash", help="Model for VideoInterpreter"
    )
    parser.add_argument(
        "--doc-evaluator-model", type=str, default="deepseek/deepseek-reasoner", help="Model for DocEvaluator"
    )
    
    args = parser.parse_args()
    
    # Check if video file exists
    if not os.path.exists(args.video_path):
        print(f"Error: Video file '{args.video_path}' not found.")
        sys.exit(1)
    
    # Create output and temp directories if they don't exist
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.temp_dir, exist_ok=True)
    
    # Create configuration
    config = VideoInstructorConfig(
        doc_generator_config=DocGeneratorConfig(
            model=args.doc_generator_model,
            temperature=0.7,
            max_output_tokens=4000
        ),
        video_interpreter_config=VideoInterpreterConfig(
            model=args.video_interpreter_model,
            temperature=0.7
        ),
        doc_evaluator_config=DocEvaluatorConfig(
            model=args.doc_evaluator_model,
            temperature=0.2,
            max_rejection_count=3
        ),
        user_feedback_interval=args.user_feedback_interval,
        max_iterations=args.max_iterations,
        output_dir=args.output_dir,
        temp_dir=args.temp_dir
    )
    
    # Initialize VideoInstructor
    instructor = VideoInstructor(config)
    
    # Process the video
    video_path = Path(args.video_path)
    output_path = instructor.process_video(video_path)
    
    print(f"Documentation generated successfully: {output_path}")


if __name__ == "__main__":
    main() 