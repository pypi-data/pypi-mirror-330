from pydantic import BaseModel, Field
from typing import Optional
from ..transfers.parameter import DateFilter, SortColumn

class GetQueryParameters(BaseModel):
    is_active:Optional[bool] = Field(None, description="Filter results based on active status.")
    is_deleted:Optional[bool] = Field(None, description="Filter results based on deletion status.")
    page:int = Field(1, ge=1, description="Page number, must be >= 1.")
    limit:int = Field(10, gt=0, le=1000, description="Page size, must be 0 < limit <= 1000.")
    search:Optional[str] = Field(None, description="Search parameter string.")

class GetBody(BaseModel):
    date_filters:list[DateFilter] = Field([], description="List of date filters to apply.")
    sort_columns:list[SortColumn] = Field([], description="List of columns to sort by.")