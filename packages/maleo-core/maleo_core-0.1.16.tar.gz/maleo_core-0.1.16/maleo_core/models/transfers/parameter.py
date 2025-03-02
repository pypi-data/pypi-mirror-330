from datetime import datetime
from pydantic import BaseModel
from typing import Literal, Optional

class DateFilter(BaseModel):
    name:str
    start:Optional[datetime] = None
    end:Optional[datetime] = None

class SortColumn(BaseModel):
    name:str
    order:Literal["asc", "desc"] = "asc"

class Get(BaseModel):
    is_active:Optional[bool] = None
    is_deleted:Optional[bool] = None
    page:int = 1
    limit:int = 10
    search:Optional[str] = None
    date_filters:list[DateFilter] = []
    sort_columns:list[SortColumn] = []

    class Config:
        arbitrary_types_allowed = True