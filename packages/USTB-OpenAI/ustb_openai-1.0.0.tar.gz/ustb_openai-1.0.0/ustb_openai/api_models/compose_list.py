from .compose_detail import ComposeItem
from .._models import ListResponseModel


class ComposeList(ListResponseModel[ComposeItem]):
    """`GET /site/ai/compose_list`
    - `classid` (number)
    """
