# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["FileCreateParams"]


class FileCreateParams(TypedDict, total=False):
    filename: Required[str]
    """File name with extension"""

    folder: str
    """Folder path (optional)"""

    kind: Literal["video", "image", "audio"]
    """Type of media file"""
