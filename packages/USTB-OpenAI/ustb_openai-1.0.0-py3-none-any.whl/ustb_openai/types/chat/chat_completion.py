from typing import List, Optional
from pydantic import BaseModel, Field
import time


class ChatContent(BaseModel):
    role: str = ""
    content: str = ""


class ChatChoice(BaseModel):
    index: int = 0
    delta: ChatContent = ChatContent(role="assistant", content="")
    message: ChatContent = ChatContent(role="assistant", content="")
    finish_reason: Optional[str] = None


class ChatCompletion(BaseModel):
    id: str = ""
    object: str = ""
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    choices: List[ChatChoice] = [ChatChoice()]
