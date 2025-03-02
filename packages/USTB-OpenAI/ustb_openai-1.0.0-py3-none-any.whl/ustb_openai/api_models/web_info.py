from typing import Dict

from pydantic import BaseModel, Field

from .._models import ResponseModel


class FileList(BaseModel):
    file_rcn: str


class OperationManual(BaseModel):
    filelist: FileList


class ImageConfig(BaseModel):
    image_rcn: str


class PcConfig(BaseModel):
    image: ImageConfig


class WebConfig(BaseModel):
    image: ImageConfig


class BackgroundImage(BaseModel):
    pc_config: PcConfig
    web_config: WebConfig


class AuthList(BaseModel):
    AigcManage: str
    knowledgeBaseManage: str
    AppManage: str
    SystemManage: str


class WebInfoItem(BaseModel):
    web_logo: str
    login_logo: str
    aq_logo: str
    brow_logo: str
    web_name: str
    water_mark: str
    web_desc: str
    login_back: str
    address: str
    record_info: str
    copyright: str
    email: str
    reply: str
    avatar_show: str
    feedback_open: str
    helper_open: str
    website_feedback: int
    welcome: str
    theme_color: str
    need_read: str
    disclaimer: str
    operation_manual: OperationManual
    isCas: bool
    schema_: str = Field(alias="schema")
    host: str
    imghost: str
    envname: str
    cookie_login_key: str
    auth_list: Dict[str, str]
    is_index_show: int
    qr: str
    qr_name: str
    web_logo_rcn: str
    login_logo_rcn: str
    aq_logo_rcn: str
    login_back_rcn: str
    brow_logo_rcn: str
    background_image: BackgroundImage = Field(alias="backgroup_image")


class WebInfo(ResponseModel[WebInfoItem]):
    """`GET /common/web_info`
    """
