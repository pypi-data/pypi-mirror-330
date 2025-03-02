from videoinstruct.videoinstructor import VideoInstructor, VideoInstructorConfig
from videoinstruct.agents.DocGenerator import DocGenerator, DocGeneratorConfig
from videoinstruct.agents.VideoInterpreter import VideoInterpreter, VideoInterpreterConfig
from videoinstruct.agents.DocEvaluator import DocEvaluator, DocEvaluatorConfig
from videoinstruct.agents.ScreenshotAgent import ScreenshotAgent, ScreenshotAgentConfig
from videoinstruct.prompt_loader import (
    DOC_GENERATOR_SYSTEM_PROMPT, 
    DOC_EVALUATOR_SYSTEM_PROMPT,
    SCREENSHOT_AGENT_SYSTEM_PROMPT
)

# Version of the package
__version__ = "0.1.2"

__all__ = [
    'VideoInstructor',
    'VideoInstructorConfig',
    'DocGenerator',
    'DocGeneratorConfig',
    'VideoInterpreter',
    'VideoInterpreterConfig',
    'DocEvaluator',
    'DocEvaluatorConfig',
    'ScreenshotAgent',
    'ScreenshotAgentConfig',
    'DOC_GENERATOR_SYSTEM_PROMPT',
    'DOC_EVALUATOR_SYSTEM_PROMPT',
    'SCREENSHOT_AGENT_SYSTEM_PROMPT',
    '__version__'
]
