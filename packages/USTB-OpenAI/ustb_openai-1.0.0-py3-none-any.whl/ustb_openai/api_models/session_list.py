from pydantic import BaseModel

from .compose_detail import ComposeItem
from .._models import ListResponseModel


class SessionItem(BaseModel):
    id: int
    sess_id: str
    uid: int
    compose_id: int
    create_time: str
    update_time: str
    ext: str
    last_content: str
    is_delete: int
    youke_sign: str
    ai_compose: ComposeItem


class SessionList(ListResponseModel[SessionItem]):
    """`GET /site/voom/session_list`
    - `page` (number)
    - `pageSize` (number)
    """
