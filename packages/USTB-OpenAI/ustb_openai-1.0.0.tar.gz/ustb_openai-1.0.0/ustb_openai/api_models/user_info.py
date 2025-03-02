from pydantic import BaseModel

from .._models import ResponseModel


class UserInfoItem(BaseModel):
    account: str
    type_name: str
    uid: int
    user_name: str
    user_number: str
    identity_name: str


class UserInfo(ResponseModel[UserInfoItem]):
    """`GET /site/user_info`
    """
