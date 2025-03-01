from __future__ import annotations

from pydantic import BaseModel

from .common import PostObject


class ModelDef(BaseModel):
    origin: str
    quantisation: str


class PostModel(PostObject):
    data: ModelDef
