from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field

from .._models import ResponseModel


class ComposeChatItem(BaseModel):
    type: str
    answer: str
    url: str
    message_id: str
    id: str
    recommend_data: List[Any] = Field(default_factory=list)
    source: List[Any] = Field(default_factory=list)
    ext: Union[List[Any], Dict[str, Any]] = Field(default_factory=list)


class ComposeChat(ResponseModel[ComposeChatItem]):
    """`POST /site/ai/compose_chat` -> **SSE**
    - `content` (string)
    - `history` (list)
      - `role` (string)
      - `content` (string)
    - `compose_id` (number)
    - `deep_search` (number)
    - `internet_search` (number)
    """
