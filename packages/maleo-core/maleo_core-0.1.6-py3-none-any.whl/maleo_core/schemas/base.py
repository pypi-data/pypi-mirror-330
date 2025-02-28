from datetime import date
from pydantic import BaseModel, Field
from typing import Literal, Optional, Any

from maleo_core.models.dto import BaseDTO

class Base:
    #* ----- ----- ----- Base Request ----- ----- ----- *#
    class GetQueryParameters(BaseModel):
        created_from:Optional[date] = None
        created_until:Optional[date] = None
        updated_from:Optional[date] = None
        updated_until:Optional[date] = None
        sort_by:Literal["id", "created_at", "updated_at"] = "id"
        sort_order:Literal["asc", "desc"] = "asc"
        page:int = Field(1, ge=1, description="Page number, must be >= 1")
        limit:int = Field(10, gt=0, description="Page size, must be > 0")

    class GetBody(BaseModel):
        date_filters:Optional[list[BaseDTO.DateFilter]] = Field(None)
        is_active:Optional[bool] = Field(None)
        is_deleted:Optional[bool] = Field(None)
        sort_columns:list[BaseDTO.SortColumn] = Field(None)
        page:int = 1
        limit:int = 10
        q:Optional[str] = None

    #* ----- ----- ----- Base Response ----- ----- ----- *#
    class Response(BaseModel):
        success:Literal[True, False]
        code:str
        message:str
        description:str

    #* ----- ----- ----- Derived Response ----- ----- ----- *#
    class FailResponse(Response):
        success:Literal[False] = False
        other:Optional[Any] = None

    class SingleDataResponse(Response):
        success:Literal[True] = True
        data:Any
        other:Optional[Any] = None

    class MultipleDataResponse(Response):
        success:Literal[True] = True
        data:list[Any]
        pagination:BaseDTO.Pagination
        other:Optional[Any] = None