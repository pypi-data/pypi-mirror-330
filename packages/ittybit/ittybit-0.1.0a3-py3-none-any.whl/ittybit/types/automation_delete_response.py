# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AutomationDeleteResponse", "Meta"]


class Meta(BaseModel):
    id: Optional[str] = None

    method: Optional[str] = None

    status: Optional[int] = None

    url: Optional[str] = None


class AutomationDeleteResponse(BaseModel):
    data: Optional[object] = None
    """Response data"""

    meta: Optional[Meta] = None
