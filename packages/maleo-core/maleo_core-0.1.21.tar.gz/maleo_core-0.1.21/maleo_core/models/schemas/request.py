from pydantic import BaseModel, Field
from typing import Literal
from ..transfers.parameter import GetQueryParameters, GetBody, StatusUpdateQueryParameter

class Request:
    GetQueryParameters = GetQueryParameters
    GetBody = GetBody
    StatusUpdateQueryParameter = StatusUpdateQueryParameter