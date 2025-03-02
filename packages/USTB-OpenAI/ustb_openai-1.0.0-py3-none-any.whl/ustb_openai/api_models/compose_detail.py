from typing import Any, Optional, Union

from pydantic import BaseModel

from .._models import ResponseModel


class ComposeItem(BaseModel):
    id: int
    name: str
    logo: str
    desc: str
    details: str
    status: int
    welcome_message: str
    unanswerable_message: str
    is_show_logo: int
    is_default_app: int
    doc_ids: Any
    plugin_ids: Any
    model_ids: Any
    creator: int
    create_time: str
    update_time: str
    sort: int
    classid: int
    content_type: int
    is_delete: int
    character_set: str
    sf_id: str
    bottom_tip: str
    type: int
    url: str
    pc_url: str
    url_download: str
    unanswerable_recommend_message: str
    auth_num: int
    usable: str
    auth_userid: Any
    open_model: int
    match_num: int
    biaoqian: str
    is_stream: int
    switch_data: Union[str, dict]
    flow_id: int
    static_logo: Optional[str] = None


class ComposeDetail(ResponseModel[ComposeItem]):
    """`GET /site/ai/compose_detail`
    - `id` (number)
    """
