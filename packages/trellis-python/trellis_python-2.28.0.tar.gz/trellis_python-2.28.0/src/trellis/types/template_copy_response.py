# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["TemplateCopyResponse", "Data"]


class Data(BaseModel):
    id: str

    proj_id: str

    transform_id: Optional[str] = None


class TemplateCopyResponse(BaseModel):
    data: Data

    message: str
