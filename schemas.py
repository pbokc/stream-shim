from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Role = Literal["system", "user", "assistant"]


class ChatMessage(BaseModel):
    role: Role
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description="Model name (for logging only in MVP)")
    messages: List[ChatMessage]
    stream: Optional[bool] = True
    temperature: Optional[float] = None
    top_p: Optional[float] = None
