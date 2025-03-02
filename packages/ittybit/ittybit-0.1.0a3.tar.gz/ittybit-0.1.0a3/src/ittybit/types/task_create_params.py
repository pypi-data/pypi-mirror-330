# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TaskCreateParams"]


class TaskCreateParams(TypedDict, total=False):
    kind: Required[str]

    input: object

    url: str
