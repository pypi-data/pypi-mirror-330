# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["FileListResponse", "Data", "Pagination"]


class Data(BaseModel):
    id: Optional[str] = None

    filename: Optional[str] = None

    folder: Optional[str] = None

    media_id: Optional[str] = None

    url: Optional[str] = None


class Pagination(BaseModel):
    limit: Optional[int] = None

    page: Optional[int] = None

    pages: Optional[int] = None

    total: Optional[int] = None


class FileListResponse(BaseModel):
    data: Optional[List[Data]] = None

    pagination: Optional[Pagination] = None
