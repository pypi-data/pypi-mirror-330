from typing import List, Optional, Dict, Any, ClassVar
from pydantic import BaseModel, Field

from videoinstruct.prompt_loader import (
    DOC_GENERATOR_SYSTEM_PROMPT, 
    DOC_EVALUATOR_SYSTEM_PROMPT,
    SCREENSHOT_AGENT_SYSTEM_PROMPT
)


class VideoInterpreterConfig(BaseModel):
    """Configuration for the VideoInterpreter class."""
    api_key: Optional[str] = None
    model: str = Field(default="gemini-2.0-flash")
    system_instruction: Optional[str] = None
    max_output_tokens: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    temperature: Optional[float] = None
    response_mime_type: Optional[str] = None
    stop_sequences: Optional[List[str]] = None
    seed: Optional[int] = None


class DocGeneratorConfig(BaseModel):
    """Configuration for the DocGenerator class."""
    api_key: Optional[str] = None
    model_provider: str = Field(default="openai")
    model: str = Field(default="o3-mini")
    system_instruction: str = Field(default=DOC_GENERATOR_SYSTEM_PROMPT)
    max_output_tokens: Optional[int] = None
    temperature: float = Field(default=0.7)
    top_p: Optional[float] = None
    stream: bool = Field(default=False)
    seed: Optional[int] = None
    response_format: Optional[Dict[str, Any]] = Field(default={"type": "json_object"})


class DocEvaluatorConfig(BaseModel):
    """Configuration for the DocEvaluator class."""
    api_key: Optional[str] = None
    model_provider: str = Field(default="deepseek")
    model: str = Field(default="deepseek-reasoner")
    system_instruction: str = Field(default=DOC_EVALUATOR_SYSTEM_PROMPT)
    max_output_tokens: Optional[int] = None
    temperature: float = Field(default=0.2)
    top_p: Optional[float] = None
    stream: bool = Field(default=False)
    seed: Optional[int] = None
    max_rejection_count: int = Field(default=3)


class ScreenshotAgentConfig(BaseModel):
    """Configuration for the ScreenshotAgent class."""
    api_key: Optional[str] = None
    model: str = Field(default="gemini-2.0-flash")
    system_instruction: str = Field(default=SCREENSHOT_AGENT_SYSTEM_PROMPT)
    max_output_tokens: Optional[int] = None
    temperature: float = Field(default=0.2)
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    seed: Optional[int] = None


class ResponseType(BaseModel):
    """Enum-like class for response types from DocGenerator."""
    DOCUMENTATION: ClassVar[str] = "documentation"
    QUESTION: ClassVar[str] = "question"


class DocGeneratorResponse(BaseModel):
    """Structured response from DocGenerator."""
    type: str  # One of ResponseType values
    content: str  # Documentation content or question
    confidence: Optional[float] = None  # Confidence level (0-1) if applicable


class VideoInstructorConfig(BaseModel):
    """Configuration for the VideoInstructor class."""
    doc_generator_config: DocGeneratorConfig = Field(default_factory=DocGeneratorConfig)
    video_interpreter_config: VideoInterpreterConfig = Field(default_factory=VideoInterpreterConfig)
    doc_evaluator_config: DocEvaluatorConfig = Field(default_factory=DocEvaluatorConfig)
    screenshot_agent_config: ScreenshotAgentConfig = Field(default_factory=ScreenshotAgentConfig)
    max_iterations: int = Field(default=10)
    user_feedback_interval: int = Field(default=5)
    output_dir: str = Field(default="output")
    temp_dir: str = Field(default="temp")
    generate_pdf_for_all_versions: bool = Field(default=True)  # Whether to generate PDFs for all versions, not just final 