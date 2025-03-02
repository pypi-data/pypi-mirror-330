from typing import Literal, Optional, Any
from pydantic import BaseModel
from ..transfers.payload import Pagination

#* ----- ----- ----- Base ----- ----- ----- *#
class Base(BaseModel):
    success:Literal[True, False]
    code:str
    message:str
    description:str

#* ----- ----- ----- Derived ----- ----- ----- *#
class Fail(Base):
    success:Literal[False] = False
    other:Optional[Any] = None

class SingleData(Base):
    success:Literal[True] = True
    data:Any
    other:Optional[Any] = None

class MultipleData(Base):
    success:Literal[True] = True
    data:list[Any]
    pagination:Pagination
    other:Optional[Any] = None