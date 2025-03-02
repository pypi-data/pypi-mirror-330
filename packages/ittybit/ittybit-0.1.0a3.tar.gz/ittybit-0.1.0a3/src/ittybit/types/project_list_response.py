# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["ProjectListResponse", "ProjectListResponseItem"]


class ProjectListResponseItem(BaseModel):
    id: Optional[str] = None

    name: Optional[str] = None

    status: Optional[str] = None


ProjectListResponse: TypeAlias = List[ProjectListResponseItem]
