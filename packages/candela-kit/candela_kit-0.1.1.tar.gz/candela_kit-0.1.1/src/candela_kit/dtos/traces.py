from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .common import ObjectMetadata, PostObject


class TraceItem(BaseModel):
    item_type: Literal[
        "user", "sys", "chat_resp", "struct_resp", "info", "result", "wait"
    ]
    content: str


class TraceItemMetadata(ObjectMetadata):
    session_id: str


class TraceMetadata(BaseModel):
    session_id: str
    trace_id: str


class PostTraceItem(PostObject):
    data: TraceItem
    session_id: str
