from typing import Literal

from termcolor import colored

from .contexts import RunAgentCircuit, RunPipelineCircuit, RunAgentApp, RunPipelineApp
from ..client import Client
from ..dtos import ToolModule, Directive, ObjectId
from ..ignite.circuits import Circuit
from ..profiles import UserProfile, get_profiles
from ..tools.tool_extract import tool_module_from_notebook

point = colored(" • ", "cyan")


def extract(to_run: Circuit) -> ToolModule | None:
    msg = "Extracting circuit tool classes. Set auto_extract=False to skip."
    print(f'[{colored(msg, "cyan")}]')
    classes = [c for c in to_run.get_tool_classes() if c.__module__ == "__main__"]

    if len(classes) == 0:
        print("   No notebook-defined tool classes in circuit.")
        tool_module = None
    else:
        print(point + f"\n{point}".join(t.__name__ for t in classes))
        tool_module = tool_module_from_notebook(*classes)

    return tool_module


class Manager:

    def __init__(self, profile: UserProfile, slot_type: str = None, model: str = None):
        self.profile = profile
        self.client = Client.from_profile(self.profile)
        self.slot_type = slot_type or profile.default_slot_type
        self.model = model or profile.default_model

    @property
    def model_id(self) -> ObjectId:
        return self.client.get_model_metadata(self.model).obj_id

    def run_from_id(
        self,
        app_id: str,
        scope: str = "default",
        version: str = None,
        tool_module: ToolModule = None,
    ):
        obj_id = ObjectId(identifier=app_id, scope=scope, version=version)
        args = (self.client, self.slot_type, self.model_id, obj_id, tool_module)
        app = self.client.get_app(obj_id.identifier, obj_id.scope, obj_id.version)
        return RunAgentApp(*args) if app.type == "agent" else RunPipelineApp(*args)

    def run_circuit(
        self,
        circuit: Circuit,
        run_as: Literal["agent", "pipeline"],
        directive: Directive = None,
        tool_module: ToolModule = None,
        auto_extract: bool = True,
    ):
        directive = directive or Directive.empty()
        if auto_extract and tool_module is None:
            tool_module = extract(circuit)

        runner_cls = RunAgentCircuit if run_as == "agent" else RunPipelineCircuit
        return runner_cls(
            self.client, self.slot_type, self.model_id, directive, circuit, tool_module
        )

    def run(
        self,
        to_run: Circuit | str,
        run_as: Literal["agent", "pipeline"] = "agent",
        **kwargs,
    ):
        """Runs a Circuit object directly or an existing app (given the identifier and optional scope/version)

        Args:
            to_run (Circuit | str): Either a Circuit object, or an identifier string referencing an existing app
            run_as (Literal['agent', 'pipeline'], optional): Required when to_run is a Circuit, specifies whether to run as agent or pipeline. An agent is an interactive chatbot, a pipeline is a text-processing pipeline that evaluates the circuit in a single pass and returns a dict.

        Keyword Args:
            directive (Directive): directive (sys prompt) to run with when running a circuit. Defaults to empty.
            scope (str): scope to run in (defaults to "default")
            version (str): semantic version string
            tool_module (ToolModule): tool module containing tool classes to be used in the circuit. If a class with the same name is in the tool store the version in the module will override it.
            auto_extract (bool): If True, automatically extract tool modules from the circuit. Defaults to True

        Returns:
            RunAgentApp | RunPipelineApp | RunAgentCircuit | RunPipelineCircuit: Appropriate run context object given input.

        """
        if isinstance(to_run, str):
            return self.run_from_id(to_run, **kwargs)
        elif isinstance(to_run, Circuit):
            return self.run_circuit(to_run, run_as, **kwargs)
        else:
            raise TypeError(f"Expected Circuit or str, got {type(to_run).__name__}")

    def __repr__(self):
        return f"""{self.__class__.__name__}(
    user_id={self.profile.user_id}, 
    domain={self.profile.domain}, 
    slot_type={self.slot_type}, 
    model={self.model}
)"""


def manager(profile: str = None, slot_type: str = None, model: str = None) -> Manager:
    """

    Args:
        profile (str, optional): name of the profile to run as. Defaults to the currently-active user profile.
        slot_type (str, optional): slot type to run with. Defaults to profile default.
        model (str, optional): name of the model to run with. Defaults to profile default.

    Returns:
        Manager: a manager object for the specified profile.
    """
    return Manager(
        profile=get_profiles().get(profile), slot_type=slot_type, model=model
    )
