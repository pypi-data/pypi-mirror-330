from __future__ import annotations

from typing import List

import black
from pydantic import BaseModel
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer

from .common import PostObject, ObjectMetadata


class ToolModule(BaseModel):
    content: str

    def __repr__(self) -> str:
        content = black.format_str(self.content, mode=black.FileMode())
        return highlight(content, PythonLexer(), Terminal256Formatter())


class PostToolModule(PostObject):
    data: ToolModule


class ToolModuleMetadata(ObjectMetadata):
    tools: List[str]


class ToolMetadata(BaseModel):
    tool_name: str
    scope: str
    module_name: str
    module_version: str
