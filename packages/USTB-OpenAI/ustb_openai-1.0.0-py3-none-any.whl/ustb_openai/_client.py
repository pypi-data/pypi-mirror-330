from typing import Optional, Type, TypeVar, Union

import httpx

from ._models import ResponseModel
from ._exceptions import APIError
from .resources.chat.chat import Chat
from .resources.info.info import Info

T = TypeVar('T')


class USTBOpenAI:
    DEFAULT_BASE_URL = "http://chat.ustb.edu.cn"
    DEFAULT_TIMEOUT = httpx.Timeout(30.0)

    chat: Chat
    info: Info
    _easy_session: str
    _client: httpx.Client

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        easy_session: Optional[str] = None,
        vjuid_login: Optional[str] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = DEFAULT_TIMEOUT,
        **kwargs_ignored
    ) -> None:
        """Initializes a USTB OpenAI client.

        :param base_url: The base URL to the AI assistant webpage of USTB;
        :param easy_session: The cookie value of `easy_session` (no-login mode), leave `None` to auto apply a new one;
        :param vjuid_login: The cookie value of `cookie_vjuid_login` (login-mode);
        :param timeout: The timeout (seconds) on all API operations;
        """
        self._client = httpx.Client()
        self._client.base_url = base_url
        self._client.timeout = httpx.Timeout(timeout)

        if not easy_session:
            pass  # Do nothing, because the user_info API will auto set a cookie with a new easy_session
        else:
            if len(easy_session) != 32 or not easy_session.isalnum():
                raise ValueError("Easy session must have 32 alpha-numeric characters")
            self._client.cookies["easy_session"] = easy_session.lower()

        if vjuid_login:
            self._client.cookies["cookie_vjuid_login"] = vjuid_login

        self.chat = Chat(self)
        self.info = Info(self)

    @property
    def easy_session(self) -> str:
        return self._client.cookies["easy_session"]

    @property
    def vjuid_login(self) -> str:
        return self._client.cookies["cookie_vjuid_login"]

    def _api_get(
        self,
        api_model: Type[ResponseModel[T]],
        api_endpoint: str,
        params: Optional[httpx._types.QueryParamTypes] = None,
    ) -> ResponseModel[T]:
        rsp = self._client.get(api_endpoint, params=params).raise_for_status()
        data = rsp.json()
        if not isinstance(data, dict):
            raise APIError("Expected JSON dict response")
        if data.get("e", None) != 0:
            raise APIError("Bad API error code", data.get("e", None), data.get("m", None))
        return api_model.model_validate(data)
