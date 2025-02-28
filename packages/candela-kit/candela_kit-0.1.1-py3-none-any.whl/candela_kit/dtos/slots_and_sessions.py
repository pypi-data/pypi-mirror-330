from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, StrictStr

from .common import ObjectId, PostObject
from .directives import Directive
from .tools import ToolModule
from ..ignite.circuits import Circuit


class SlotsPutResponse(BaseModel):
    """Response model for a put response where the response sends previous value
    along with updated value
    """

    old_value: int
    new_value: int


class Session(BaseModel):

    model_config = ConfigDict(protected_namespaces=())

    app: ObjectId | None
    model_cfg: ObjectId

    host_id: str
    parent_session: Optional[ObjectId] = None
    circuit_override: Optional[ObjectId] = None
    directive_override: Optional[ObjectId] = None

    dev_session: Optional[bool] = False


class PostSession(PostObject):

    data: Session


class SessionStartRequest(BaseModel):

    model_config = ConfigDict(protected_namespaces=())

    app: ObjectId
    model_cfg: ObjectId

    scope: Optional[str] = "default"
    parent_session: Optional[ObjectId] = None
    circuit_override: Optional[ObjectId] = None
    directive_override: Optional[ObjectId] = None


class DevSessionStartRequest(BaseModel):

    model_config = ConfigDict(protected_namespaces=())

    model_id: ObjectId
    circuit: Circuit
    directive: Directive

    scope: Optional[str] = "default"
    parent_session: Optional[ObjectId] = None
    tool_module_override: Optional[ToolModule] = None


class SubmitPrompt(BaseModel):
    prompt: str
    session_id: str


class Event(BaseModel):
    event_type: Literal["chat", "intent", "info", "result", "wait", "user", "sys"]
    content: StrictStr


class SlotState(Enum):

    START_REQUEST = 0
    NODE_STARTING = 1
    HOST_STARTING = 2
    HOST_READY = 3
    STOPPING = 4
    HOST_DISPOSED = 5
    ERRORED = 6
    HOST_GONE = 7
    HOST_IDLE = 8


class SlotData(BaseModel):

    slot_id: str
    slot_type: str
    domain: str

    state: SlotState = SlotState.START_REQUEST

    assigned_to: str | None = None
    url: str | None = None

    created: datetime | None = None
    assigned: datetime | None = None
    disposed: datetime | None = None
    ready: datetime | None = None
