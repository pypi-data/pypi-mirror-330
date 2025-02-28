from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, field_serializer, model_validator
from typing import Literal, Optional, Any
from uuid import UUID

from maleo_core.utils.constants import REFRESH_TOKEN_DURATION_DAYS, ACCESS_TOKEN_DURATION_MINUTES

class Base:
    #* ----- ----- Token ----- ----- *#
    class TokenPayload(BaseModel):
        uuid:UUID
        scope:Literal["refresh", "access"]
        iat:datetime
        exp:datetime

        @model_validator(mode="before")
        def set_iat_and_exp(cls, values:dict):
            iat = values.get("iat", None)
            exp = values.get("iat", None)
            if not iat and not exp:
                iat = datetime.now(timezone.utc)
                values["iat"] = iat
                if values["scope"] == "refresh":
                    values["exp"] = iat + timedelta(days=REFRESH_TOKEN_DURATION_DAYS)
                elif values["scope"] == "access":
                    values["exp"] = iat + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)
            return values

    #* ----- ----- Authorization ----- ----- *#
    class ValidateResult(BaseModel):
        authorized:Literal[False, True]
        response:Optional[JSONResponse] = None
        token:Optional[str] = None

        class Config:
            arbitrary_types_allowed = True

    #* ----- ----- Base Parameters ----- ----- *#
    class DateFilter(BaseModel):
        name:str
        start:Optional[datetime] = None
        end:Optional[datetime] = None

    class SortColumn(BaseModel):
        name:str
        order:Literal["asc", "desc"] = "asc"

    class GetParameters(BaseModel):
        date_filters:list['Base.DateFilter'] = []
        is_active:bool = True
        is_deleted:bool = False
        sort_columns:list['Base.SortColumn'] = []
        page:int = 1
        limit:int = 10
        q:Optional[str] = None

        class Config:
            arbitrary_types_allowed = True

    class GetResults(BaseModel):
        id:int
        created_at:datetime
        updated_at:datetime
        is_active:bool
        is_deleted:bool

        @field_validator('*', mode="before")
        def set_none(cls, v):
            if isinstance(v, str) and (v == "" or len(v) == 0):
                return None
            return v

        @field_serializer('*')
        def serialize_values(self, v):
            if isinstance(v, datetime):
                return v.isoformat()
            return v

        class Config:
            from_attributes=True

    class Pagination(BaseModel):
        page_number:int = 1
        data_count:int = 0
        total_data:int = 0
        total_pages:int = 1

    class SingleQueryResult(BaseModel):
        data:Optional[Any]

    class MultipleQueryResult(BaseModel):
        data:list[Any]
        data_count:int
        total_data:int

    class SingleDataResult(BaseModel):
        data:Optional[Any]

    class MultipleDataResult(BaseModel):
        data:list[Any]
        pagination:'Base.Pagination'

    class ControllerResult(BaseModel):
        success:Literal[True, False]
        response:Optional[JSONResponse]

        class Config:
            arbitrary_types_allowed=True

Base.GetParameters.model_rebuild()
Base.GetResults.model_rebuild()
Base.Pagination.model_rebuild()
Base.MultipleDataResult.model_rebuild()