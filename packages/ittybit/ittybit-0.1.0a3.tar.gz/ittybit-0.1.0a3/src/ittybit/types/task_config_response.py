# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TaskConfigResponse", "Formats", "Meta"]


class Formats(BaseModel):
    input: Optional[List[str]] = None

    output: Optional[List[str]] = None


class Meta(BaseModel):
    id: Optional[str] = None

    method: Optional[str] = None

    status: Optional[int] = None

    url: Optional[str] = None


class TaskConfigResponse(BaseModel):
    data: Optional[object] = None
    """Response data"""

    formats: Optional[Formats] = None

    meta: Optional[Meta] = None

    qualities: Optional[List[Literal["low", "medium", "high"]]] = None

    types: Optional[List[Literal["transform", "analyze"]]] = None
