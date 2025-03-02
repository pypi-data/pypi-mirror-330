from datetime import date
from pydantic import BaseModel, Field
from typing import Literal, Optional
from ..transfers.parameter import DateFilter, SortColumn

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
    date_filters:list[DateFilter] = []
    is_active:Optional[bool] = None
    is_deleted:Optional[bool] = None
    sort_columns:list[SortColumn] = []
    page:int = 1
    limit:int = 10
    q:Optional[str] = None