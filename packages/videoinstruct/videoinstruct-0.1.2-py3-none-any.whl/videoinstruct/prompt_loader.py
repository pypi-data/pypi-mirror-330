"""
This module loads system prompts from text files in the prompts directory.
"""
from pathlib import Path

# Get the directory where this file is located
CURRENT_DIR = Path(__file__).parent
PROMPTS_DIR = CURRENT_DIR / "prompts"

def load_prompt(filename):
    """
    Load a prompt from a text file in the prompts directory.
    
    Args:
        filename (str): The name of the text file (without directory path)
        
    Returns:
        str: The content of the prompt file
    """
    file_path = PROMPTS_DIR / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Load all prompts
DOC_GENERATOR_SYSTEM_PROMPT = load_prompt("doc_generator.txt")
DOC_EVALUATOR_SYSTEM_PROMPT = load_prompt("doc_evaluator.txt")
SCREENSHOT_AGENT_SYSTEM_PROMPT = load_prompt("screenshot_agent.txt")

# Add any additional prompts here as they are created 