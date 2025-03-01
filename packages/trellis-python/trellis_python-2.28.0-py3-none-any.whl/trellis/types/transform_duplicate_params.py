# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["TransformDuplicateParams"]


class TransformDuplicateParams(TypedDict, total=False):
    copy_assets: bool
    """Copy the assets over from the old transformation."""
