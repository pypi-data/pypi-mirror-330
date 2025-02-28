from __future__ import annotations

import json
from enum import Enum
from typing import List, Optional, Dict, TypeVar, Type, Iterator, Literal

import requests as r
from pandas import DataFrame
from pydantic import BaseModel
from requests import Response
from tqdm import tqdm

from .dtos import (
    App,
    PostApp,
    ObjectId,
    ObjectMetadata,
    PostCircuit,
    Directive,
    PostDirective,
    Event,
    Session,
    SlotData,
    SlotState,
    SubmitPrompt,
    SessionStartRequest,
    DevSessionStartRequest,
    ToolModule,
    ToolModuleMetadata,
    ToolMetadata,
    PostToolModule,
    TraceItem,
    TraceMetadata,
)
from .exceptions import CandelaApiError
from .ignite.circuits import Circuit
from .profiles import get_profiles, UserProfile
from datetime import datetime

TMeta = TypeVar("TMeta", bound=ObjectMetadata)
TObj = TypeVar("TObj", bound=BaseModel)


def map_col_type(df):
    exemplar = df.iloc[0].to_dict()
    for k, v in exemplar.items():
        if issubclass(type(v), Enum):
            df[k] = df[k].apply(lambda x: x.name)
        elif issubclass(type(v), datetime):
            df[k] = df[k].dt.round("s").dt.tz_localize(None)
    return df


def models_to_df(models: Iterator[BaseModel]) -> DataFrame:

    def flatten(x):
        x = x.model_dump()
        add_props = x.pop("additional_properties", {})
        obj_id = x.pop("obj_id", {})
        obj_id.pop("additional_properties", {})
        return {**obj_id, **x, **add_props}

    df = DataFrame(flatten(s) for s in models)

    if len(df) > 0:
        df = map_col_type(df)
    return df


class Client:

    def __init__(
        self, access_token: str, api_url: str, domain_override: str | None = None
    ):
        self.access_token = access_token
        self.domain_override = domain_override
        if api_url.endswith("/"):
            api_url = api_url.rstrip("/")
        self.api_url = api_url

    def _headers(self) -> Dict:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        if self.domain_override is not None:
            headers["Host"] = f"{self.domain_override}.lusid.com/candela"
        return headers

    @staticmethod
    def raise_for_status(response: Response):
        if isinstance(response, Response):
            if not response.ok:
                raise CandelaApiError.from_requests_response(response)
        else:
            raise TypeError(
                f"Unexpected response type in raise_for_status: {type(response).__name__}"
            )

    def __repr__(self):
        name = type(self).__name__
        n = 10
        if self.access_token == "local":
            censored_token = "NA"
        else:
            censored_token = f'{self.access_token[:3]}{n * "-"}{self.access_token[-5:]}'
        return f"{name}(\n    token: {censored_token},\n    api_url: {self.api_url}\n)"

    def set_free_slots_target(self, slot_type: str, free_slots: int) -> Dict[str, int]:
        params = {"slot_type": slot_type, "target_free_slots": free_slots}
        res = r.put(
            self.api_url + "/system/free_slots_target",
            params=params,
            headers=self._headers(),
        )
        self.raise_for_status(res)
        return res.json()

    def set_max_slots(self, slot_type: str, max_slots: int) -> Dict[str, int]:
        params = {"slot_type": slot_type, "max_slots": max_slots}
        res = r.put(
            self.api_url + "/system/max_slots", params=params, headers=self._headers()
        )
        self.raise_for_status(res)
        return res.json()

    def list_slots(self) -> DataFrame:
        res = r.get(self.api_url + "/system/list_slots", headers=self._headers())
        self.raise_for_status(res)
        return models_to_df(SlotData.model_validate(m) for m in res.json())

    def get_system_status(self) -> Dict[str, Dict]:
        res = r.get(self.api_url + "/system/status", headers=self._headers())
        self.raise_for_status(res)
        return res.json()

    def admin_delete_slot(self, slot_id: str):
        params = {"slot_id": slot_id}
        res = r.delete(
            self.api_url + "/system/slot", params=params, headers=self._headers()
        )
        self.raise_for_status(res)

    # region slots_management
    def has_slot(self) -> bool:
        res = r.get(self.api_url + "/slot/user_has_slot", headers=self._headers())
        self.raise_for_status(res)
        return res.json()

    def assign_slot(self, slot_type):
        res = r.put(
            self.api_url + "/slot",
            params={"slot_type": slot_type},
            headers=self._headers(),
        )
        self.raise_for_status(res)

    def dispose_slot(self):
        res = r.delete(self.api_url + "/slot", headers=self._headers())
        self.raise_for_status(res)

    def get_slot_state(self) -> SlotState:
        res = r.get(self.api_url + "/slot/state", headers=self._headers())
        self.raise_for_status(res)
        return SlotState(res.json())

    def get_slot_metadata(self) -> SlotData:
        res = r.get(self.api_url + "/slot/metadata", headers=self._headers())
        self.raise_for_status(res)
        return SlotData.model_validate(res.json())

    # endregion

    # region session_management
    def start_dev_session(
        self,
        circuit: Circuit,
        directive: Directive,
        model: ObjectId,
        scope: Optional[str] = "default",
        parent_session_id: Optional[str] = None,
        tool_module_override: Optional[ToolModule] = None,
    ) -> ObjectMetadata:
        req = DevSessionStartRequest(
            circuit=circuit,
            directive=directive,
            model_id=model,
            scope=scope,
            parent_session=parent_session_id,
            tool_module_override=tool_module_override,
        )
        url = self.api_url + "/session/dev"
        res = r.post(url, json=req.model_dump(), headers=self._headers())
        self.raise_for_status(res)
        return ObjectMetadata.model_validate(res.json())

    def start_session(
        self,
        app: ObjectId,
        model: ObjectId,
        scope: Optional[str] = "default",
        parent_session_id: Optional[ObjectId] = None,
        circuit_override: Optional[ObjectId] = None,
        directive_override: Optional[ObjectId] = None,
    ) -> ObjectMetadata:

        req = SessionStartRequest(
            app=app,
            model_cfg=model,
            scope=scope,
            parent_session=parent_session_id,
            circuit_override=circuit_override,
            directive_override=directive_override,
        )
        res = r.post(
            self.api_url + "/session", json=req.model_dump(), headers=self._headers()
        )
        self.raise_for_status(res)
        return ObjectMetadata.model_validate(res.json())

    def stop_session(self):
        url = self.api_url + "/session/stop"
        res = r.get(url, headers=self._headers())
        self.raise_for_status(res)

    def submit_prompt_to_agent(self, prompt: str, session_id: str) -> Iterator[Event]:
        url = self.api_url + "/session/agent_submit"
        req = SubmitPrompt(prompt=prompt, session_id=session_id)
        with r.post(
            url, json=req.model_dump(), stream=True, headers=self._headers()
        ) as res:
            self.raise_for_status(res)
            for line in res.iter_lines(chunk_size=1024):
                yield Event.model_validate_json(line)

    def submit_prompt_to_pipeline(self, prompt: str, session_id: str) -> Dict:
        url = self.api_url + "/session/pipeline_submit"
        req = SubmitPrompt(prompt=prompt, session_id=session_id)
        res = r.post(url, json=req.model_dump(), headers=self._headers())
        self.raise_for_status(res)
        return res.json()

    # endregion

    # region crud_util_methods

    def _list(self, url, all_versions, meta_cls: Type[TMeta]) -> DataFrame:
        params = {"all_versions": all_versions}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return models_to_df(meta_cls.model_validate(v) for v in res.json())

    def _get(self, url, identifier, scope, version, data_cls: Type[TObj]) -> TObj:
        params = {"identifier": identifier, "scope": scope, "version": version}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return data_cls.model_validate(res.json())

    def _get_meta(
        self, url, identifier, scope, version, meta_cls: Type[TMeta]
    ) -> TMeta:
        params = {"identifier": identifier, "scope": scope, "version": version}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return meta_cls.model_validate(res.json())

    def _del(
        self, url, identifier, scope, version, meta_cls: Type[TMeta]
    ) -> List[TMeta]:
        params = {"identifier": identifier, "scope": scope, "version": version}
        res = r.delete(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return [meta_cls.model_validate(v) for v in res.json()]

    def _exists(self, url, identifier, scope, version) -> bool:
        params = {"identifier": identifier, "scope": scope, "version": version}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return res.json()

    # endregion

    # region apps

    def add_app(
        self,
        app: App,
        identifier: str,
        scope: str = "default",
        description: str = "no description",
        version_bump: Literal["major", "minor", "patch"] = "patch",
        system_level: bool = False,
    ) -> ObjectMetadata:
        url = self.api_url + "/apps/"
        req = PostApp(
            data=app,
            scope=scope,
            identifier=identifier,
            description=description,
            version_bump=version_bump,
        )
        params = {"system_level": system_level}
        res = r.put(url, json=req.model_dump(), params=params, headers=self._headers())
        self.raise_for_status(res)
        return ObjectMetadata.model_validate(res.json())

    def list_apps(self, all_versions: bool = False) -> DataFrame:
        url = self.api_url + "/apps/list"
        return self._list(url, all_versions, ObjectMetadata)

    def get_app(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> App:
        url = self.api_url + "/apps/"
        return self._get(url, identifier, scope, version, App)

    def get_app_metadata(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> ObjectMetadata:
        url = self.api_url + "/apps/metadata"
        return self._get_meta(url, identifier, scope, version, ObjectMetadata)

    def delete_app(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> List[ObjectMetadata]:
        url = self.api_url + "/apps/"
        return self._del(url, identifier, scope, version, ObjectMetadata)

    def app_exists(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> bool:
        url = self.api_url + "/apps/exists"
        return self._exists(url, identifier, scope, version)

    # endregion

    # region circuits

    def add_circuit(
        self,
        circuit: Circuit,
        identifier: str,
        scope: Optional[str] = "default",
        description: str = "no description",
        version_bump: Literal["major", "minor", "patch"] = "patch",
        system_level: bool = False,
    ) -> ObjectMetadata:
        url = self.api_url + "/circuits/"
        req = PostCircuit(
            data=circuit,
            scope=scope,
            identifier=identifier,
            description=description,
            version_bump=version_bump,
        )
        params = {"system_level": system_level}
        res = r.put(url, json=req.model_dump(), params=params, headers=self._headers())
        self.raise_for_status(res)
        return ObjectMetadata.model_validate(res.json())

    def list_circuits(self, all_versions: bool = False) -> DataFrame:
        url = self.api_url + "/circuits/list"
        return self._list(url, all_versions, ObjectMetadata)

    def get_circuit(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> Circuit:
        url = self.api_url + "/circuits/"
        return self._get(url, identifier, scope, version, Circuit)

    def get_circuit_metadata(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> ObjectMetadata:
        url = self.api_url + "/circuits/metadata"
        return self._get_meta(url, identifier, scope, version, ObjectMetadata)

    def delete_circuit(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> List[ObjectMetadata]:
        url = self.api_url + "/circuits/"
        return self._del(url, identifier, scope, version, ObjectMetadata)

    def circuit_exists(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> bool:
        url = self.api_url + "/circuits/exists"
        return self._exists(url, identifier, scope, version)

    # endregion

    # region directives

    def add_directive(
        self,
        directive: Directive,
        identifier: str,
        scope: Optional[str] = "default",
        description: str = "no description",
        version_bump: Literal["major", "minor", "patch"] = "patch",
        system_level: bool = False,
    ) -> ObjectMetadata:
        url = self.api_url + "/directives/"
        req = PostDirective(
            data=directive,
            scope=scope,
            identifier=identifier,
            description=description,
            version_bump=version_bump,
        )
        params = {"system_level": system_level}
        res = r.put(url, json=req.model_dump(), params=params, headers=self._headers())
        self.raise_for_status(res)
        return ObjectMetadata.model_validate(res.json())

    def list_directives(self, all_versions: bool = False) -> DataFrame:
        url = self.api_url + "/directives/list"
        return self._list(url, all_versions, ObjectMetadata)

    def get_directive(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> Directive:
        url = self.api_url + "/directives/"
        return self._get(url, identifier, scope, version, Directive)

    def get_directive_metadata(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> ObjectMetadata:
        url = self.api_url + "/directives/metadata"
        return self._get_meta(url, identifier, scope, version, ObjectMetadata)

    def delete_directive(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> List[ObjectMetadata]:
        url = self.api_url + "/directives/"
        return self._del(url, identifier, scope, version, ObjectMetadata)

    def directive_exists(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> bool:
        url = self.api_url + "/directives/exists"
        return self._exists(url, identifier, scope, version)

    # endregion

    # region models

    def add_model(
        self,
        hf_url: str,
        identifier: str,
        quantisation: str,
        scope: Optional[str] = "default",
        description: str = "no description",
        version_bump: str = "patch",
        system_level: bool = False,
    ) -> ObjectMetadata:
        url = self.api_url + "/models/"
        params = {
            "hf_url": hf_url,
            "scope": scope,
            "identifier": identifier,
            "quantisation": quantisation,
            "description": description,
            "version_bump": version_bump,
            "system_level": system_level,
        }
        with r.put(url, params=params, headers=self._headers()) as res:
            self.raise_for_status(res)
            lines = map(json.loads, res.iter_lines(chunk_size=1024))
            first = next(lines)

            pbar = tqdm(
                desc="  downloading",
                total=first["details"]["total_bytes"],
                unit="b",
                unit_scale=True,
                ncols=96,
            )
            for lines in lines:
                if lines["status"] == "in_progress":
                    pbar.update(lines["details"]["written_bytes"] - pbar.n)
                elif lines["status"] == "complete":
                    pbar.close()
                    return ObjectMetadata.from_dict(lines["details"])

    def list_models(self, all_versions: bool = False) -> DataFrame:
        url = self.api_url + "/models/list"
        return self._list(url, all_versions, ObjectMetadata)

    def get_model_metadata(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> ObjectMetadata:
        url = self.api_url + "/models/metadata"
        return self._get_meta(url, identifier, scope, version, ObjectMetadata)

    def delete_model(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> List[ObjectMetadata]:
        url = self.api_url + "/models/"
        return self._del(url, identifier, scope, version, ObjectMetadata)

    def model_exists(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> bool:
        url = self.api_url + "/models/exists"
        return self._exists(url, identifier, scope, version)

    # endregion

    # region sessions

    def list_sessions(self) -> DataFrame:
        return self._list(self.api_url + "/sessions/list", False, ObjectMetadata)

    def get_session(self, identifier: str, scope: str = "default") -> Session:
        url = self.api_url + "/sessions/"
        return self._get(url, identifier, scope, None, Session)

    def get_session_metadata(
        self, identifier: str, scope: str = "default"
    ) -> ObjectMetadata:
        url = self.api_url + "/sessions/metadata"
        return self._get_meta(url, identifier, scope, None, ObjectMetadata)

    def delete_session(
        self, identifier: str, scope: str = "default"
    ) -> List[ObjectMetadata]:
        url = self.api_url + "/sessions/"
        return self._del(url, identifier, scope, None, ObjectMetadata)

    def session_exists(self, identifier: str, scope: str = "default") -> bool:
        url = self.api_url + "/sessions/exists"
        return self._exists(url, identifier, scope, None)

    # endregion

    # region tool_modules

    def add_tool_module(
        self,
        module: ToolModule,
        identifier: str,
        scope: Optional[str] = "default",
        description: str = "no description",
        version_bump: Literal["major", "minor", "patch"] = "patch",
        system_level: bool = False,
    ) -> ToolModuleMetadata:
        url = self.api_url + "/tool_modules/"
        req = PostToolModule(
            data=module,
            scope=scope,
            identifier=identifier,
            description=description,
            version_bump=version_bump,
        )
        params = {"system_level": system_level}
        res = r.put(url, json=req.model_dump(), params=params, headers=self._headers())
        self.raise_for_status(res)
        return ToolModuleMetadata.model_validate(res.json())

    def list_tool_modules(self, all_versions: bool = False) -> DataFrame:
        url = self.api_url + "/tool_modules/list"
        return self._list(url, all_versions, ToolModuleMetadata)

    def get_tool_module(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> ToolModule:
        url = self.api_url + "/tool_modules/"
        return self._get(url, identifier, scope, version, ToolModule)

    def get_tool_module_metadata(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> ToolModuleMetadata:
        url = self.api_url + "/tool_modules/metadata"
        return self._get_meta(url, identifier, scope, version, ToolModuleMetadata)

    def delete_tool_module(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> List[ToolModuleMetadata]:
        url = self.api_url + "/tool_modules/"
        return self._del(url, identifier, scope, version, ToolModuleMetadata)

    def tool_module_exists(
        self, identifier: str, scope: str = "default", version: str = None
    ) -> bool:
        url = self.api_url + "/tool_modules/exists"
        return self._exists(url, identifier, scope, version)

    def list_tools(self, all_versions: bool = False) -> DataFrame:
        url = self.api_url + "/tool_modules/tool/list"
        params = {"all_versions": all_versions}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return models_to_df(ToolMetadata.model_validate(v) for v in res.json())

    def tool_exists(self, name: str, scope: str = "default") -> bool:
        url = self.api_url + "/tool_modules/tool/exists"
        params = {"scope": scope, "name": name}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return res.json()

    def get_tool_metadata(self, name: str, scope: str = "default") -> ToolMetadata:
        url = self.api_url + "/tool_modules/tool/metadata"
        params = {"scope": scope, "name": name}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return ToolMetadata.model_validate(res.json())

    # endregion

    # region traces

    def get_trace(self, session_id: str, trace_id: str) -> List[TraceItem]:
        url = self.api_url + "/traces/"
        params = {"session_id": session_id, "trace_id": trace_id}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return [TraceItem.model_validate(v) for v in res.json()]

    def list_traces(self, session_id: str = None) -> DataFrame:
        url = self.api_url + "/traces/list"
        params = {"session_id": session_id}
        res = r.get(url, params=params, headers=self._headers())
        self.raise_for_status(res)
        return models_to_df(TraceMetadata.model_validate(v) for v in res.json())

    # endregion

    @classmethod
    def from_profile(cls, profile: UserProfile) -> Client:
        domain_override = (
            profile.domain
            if "0.0.0.0" in profile.api_url or "127.0.0.1" in profile.api_url
            else None
        )
        return Client(
            profile.access_token.get_secret_value(), profile.api_url, domain_override
        )


def client(profile_name: str = None) -> Client:
    profile = get_profiles().get(profile_name)
    return Client.from_profile(profile)
