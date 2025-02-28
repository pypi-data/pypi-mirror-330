from .common import PostObject
from ..ignite.circuits import Circuit


class PostCircuit(PostObject):
    data: Circuit
