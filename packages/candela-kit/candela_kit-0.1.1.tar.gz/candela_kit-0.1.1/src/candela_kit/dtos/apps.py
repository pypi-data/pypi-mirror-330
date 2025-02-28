from typing import Literal

from pydantic import BaseModel

from .common import PostObject, ObjectId


class App(BaseModel):
    type: Literal["agent", "pipeline"]
    circuit: ObjectId
    directive: ObjectId


class PostApp(PostObject):
    data: App
