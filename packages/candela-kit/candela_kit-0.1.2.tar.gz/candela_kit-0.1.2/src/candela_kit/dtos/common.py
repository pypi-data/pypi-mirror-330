from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class ObjectId(BaseModel):

    scope: str
    identifier: str
    version: Optional[str] = None

    def label(self):
        ver = self.version or "latest"
        return f"{self.scope}/{self.identifier}:{ver}"


class ObjectMetadata(BaseModel):

    obj_id: ObjectId
    domain: str
    created_by: str
    created_at: datetime
    description: Optional[str] = "[no description]"


class PostObject(BaseModel):

    scope: str
    identifier: str
    description: Optional[str] = "[no description]"
    version_bump: Literal["major", "minor", "patch"] = "patch"
