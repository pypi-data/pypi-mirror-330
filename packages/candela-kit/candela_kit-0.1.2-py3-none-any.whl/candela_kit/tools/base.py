import json
from queue import Queue
from typing import Optional, Dict, Callable

import lumipy as lm
from pandas import DataFrame
from pydantic import BaseModel, Field, model_validator
from pydantic.json_schema import SkipJsonSchema

from ..ignite.intent import IObj


class BaseTool(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    queue: SkipJsonSchema[Optional[Queue]] = Field(None, exclude=True)
    creds_fn: SkipJsonSchema[Optional[Callable]] = Field(None, exclude=True)
    tool_type: Optional[str] = None
    instruction: Optional[str] = Field(None)

    @model_validator(mode="before")
    def set_tool_type(cls, data):
        if isinstance(data, dict):
            data["tool_type"] = data.get("tool_type", cls.__name__)
        return data

    def intent(self) -> IObj:
        """Create the intent spec for this tool.

        Returns:
            IObj: the intent spec.
        """
        raise NotImplementedError()

    def apply(self, intent: Dict) -> DataFrame | Dict | str:
        """
        Performs an action based on the given intent.

        This method should be implemented by concrete subclasses to provide custom behavior.

        Args:
            intent (Dict): A dictionary containing information about a specific request or action.

        Returns:
            Event: An Event wrapping a dictionary containing the result of the action.
        """
        raise NotImplementedError()

    def push_wait_msg(self, msg: str | Dict):
        """Push a wait message to the queue that may have useful information about the running tool.

        Args:
            msg (str | Dict): string message or dictionary of information. Dicts will be converted to json strings.

        """
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        self.queue.put(msg)

    def lumipy_client(self):
        token, domain = self.creds_fn()
        return lm.get_client(
            access_token=token, api_url=f"https://{domain}.lusid.com/honeycomb"
        )

    def lumipy_atlas(self):
        token, domain = self.creds_fn()
        return lm.get_atlas(
            access_token=token, api_url=f"https://{domain}.lusid.com/honeycomb"
        )

    def lusid_api(self, api_cls):
        token, domain = self.creds_fn()
        from lusid import ArgsConfigurationLoader
        from lusid.extensions import SyncApiClientFactory

        cfg = ArgsConfigurationLoader(
            access_token=token, api_url=f"https://{domain}.lusid.com/api"
        )
        factory = SyncApiClientFactory(config_loaders=[cfg])
        return factory.build(api_cls)
