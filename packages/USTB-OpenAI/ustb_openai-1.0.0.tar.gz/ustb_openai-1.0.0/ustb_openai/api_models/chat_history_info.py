from typing import Any

from pydantic import BaseModel

from .._models import ListResponseModel


class ChatHistoryItem(BaseModel):
    id: int
    unid: str
    session_id: str
    content: str
    hit: int
    source: int
    extra: Any
    voom_id: Any
    raw_id: Any
    creator: int
    ct: float
    ut: int
    feedback_type: int
    feedback: str
    sensitive_words: str
    compose_id: int
    answer_message_id: str
    feedback_id: int
    client_ip: str
    avatar_sign: str


class ChatHistoryInfo(ListResponseModel[ChatHistoryItem]):
    """`GET /site/voom/chat_history_info`
    - `session_id` (string)
    """
