from pydantic import BaseModel, Field
from typing import Generic, List, TypeVar, Union

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    status: int = Field(alias="e")
    message: str = Field(alias="m")
    data: T = Field(alias="d")


class ListResponseModel(ResponseModel[List[T]], Generic[T]):
    pass


class StringResponseModel(ResponseModel[str]):
    pass


class NumberResponseModel(ResponseModel[Union[int, float]]):
    pass
