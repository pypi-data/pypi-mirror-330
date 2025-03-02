from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..._client import USTBOpenAI

from ...api_models import (
    UserInfo,
    UserInfoItem,
    WebInfo,
    WebInfoItem,
    ComposeList,
    ComposeItem,
    ComposeDetail,
    PageSetting,
    PageSettingItem
)


class Info:
    """Information set.
    """
    _client: USTBOpenAI

    def __init__(self, client: USTBOpenAI) -> None:
        self._client = client

    def get_user_info(self) -> UserInfoItem:
        """Gets current user information.
        """
        return self._client._api_get(UserInfo, "/site/user_info").data

    def get_web_info(self) -> WebInfoItem:
        """Gets webpage configuration information.
        """
        return self._client._api_get(WebInfo, "/common/web_info").data

    def get_compose_list(self) -> List[ComposeItem]:
        """Gets available AI components on the server.
        """
        return self._client._api_get(
            ComposeList,
            "/site/ai/compose_list",
            { "classid": 0 }
        ).data

    def get_compose_detail(self, compose_id: int) -> ComposeItem:
        """Gets the detailed information of the specified AI component.
        """
        return self._client._api_get(
            ComposeDetail,
            "/site/ai/compose_detail",
            { "id": compose_id }
        ).data

    def get_page_setting(self, compose_id: int, page_type: str = "pc") -> PageSettingItem:
        """Gets the webpage setting of the specified AI component.
        """
        return self._client._api_get(
            PageSetting,
            "/site/voom/page-setting",
            {
                "compose_id": compose_id,
                "type": page_type
            }
        ).data
