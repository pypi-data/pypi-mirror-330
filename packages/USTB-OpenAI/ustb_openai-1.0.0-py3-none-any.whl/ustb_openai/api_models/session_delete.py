from typing import Any

from .._models import ListResponseModel


class SessionDelete(ListResponseModel[Any]):
    """`POST /site/voom/session_delete`
    - `session_id` (string)
    """
