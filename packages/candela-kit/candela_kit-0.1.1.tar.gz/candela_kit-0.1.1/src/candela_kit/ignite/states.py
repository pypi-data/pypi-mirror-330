from __future__ import annotations

import uuid
from abc import ABC
from typing import Tuple, Callable, Union
from typing import TypeVar, List, Optional, Dict

from pydantic import BaseModel, StrictStr, Field, StrictBool, model_validator
from pydantic.json_schema import SkipJsonSchema

from ..common.common import to_snake_case
from ..ignite.intent import IObj, IArr
from ..tools.base import BaseTool

stop_signals = [
    "[/INST]",
    "[INST]",
    "<</SYS>>",
    "<<SYS>>",
    "</SYS>",
    "<SYS>",
    "</s>",
    "<</INST>>",
    "<|eot_id|>",
]


class State(ABC, BaseModel):
    """Base class for all circuit states."""

    node_id: Optional[StrictStr] = Field(None)
    node_type: Optional[StrictStr] = Field(None)
    circuit_link: SkipJsonSchema[Callable[..., None] | None] = Field(None, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    @model_validator(mode="before")
    @classmethod
    def set_fields(cls, values: dict) -> dict:
        if values.get("node_id") is None:
            values["node_id"] = str(uuid.uuid4())[:5]
        values["node_type"] = cls.__name__
        return values

    @property
    def output_id(self) -> str:
        """Get the output id for variables created by this node.

        Returns:
            str: the output id.
        """
        return f"block_{self.node_id}"

    def get_label(self) -> str:
        """Get the label of this node type

        Returns:
            str: the node type label string
        """
        return to_snake_case(self.node_type)

    def __eq__(self, other: State) -> bool:
        if not isinstance(other, type(self)):
            return False

        return self.model_dump_json() == other.model_dump_json()


TState = TypeVar("TState", bound="State")


class OpState(State, ABC):
    """Base class for operation states. Operation states are states that have a single defined output state."""

    as_block: StrictBool
    child_id: Optional[StrictStr] = None

    def link_to(self, node: TState) -> TState:
        """Link this state to a child state and add the child state to this state's circuit.

        Args:
            node (TState): the child state to be linked to.

        Returns:
            TState: the child state.

        """
        self.circuit_link(node)
        self.child_id = node.node_id
        return node

    def switch(self, **kwargs: str) -> List[NoOpState]:
        """Switch between some given cases. This is for introducing branching logic in the circuits.

        Args:
            **kwargs (str): the individual cases to branch down. The keyword is the name of the case and the string
            input is the condition associated with the case.

        Returns:
            List[NoOpState]: a list of no-op states that represent the different cases of the switch.

        """
        cdn = SwitchState(circuit_link=self.circuit_link, case_spec=kwargs)
        return self.link_to(cdn).build_cases()

    def comment(
        self, msg: str | None = None, template: str | None = None, **inserts
    ) -> ResponseState:
        """Chain a comment state after this state.

        Args:
            msg (Optional[str]): context message to form the response.
            template (Optional[str]): template to constrain the response.
            **inserts (Optional[Join | Select]): guidance objects to insert into the template.

        Returns:
            ResponseState: the response state representing the comment.

        """
        inserts = {k: str(v) for k, v in inserts.items()}
        comment = ResponseState(
            circuit_link=self.circuit_link,
            context=msg,
            template=template,
            as_block=False,
            inserts=inserts,
        )
        return self.link_to(comment)

    def tool(
        self,
        tool: BaseTool,
        ask_confirmation: Optional[bool] = True,
        confirmation_msg: Optional[bool] = True,
    ) -> UseToolState:
        """Chain a tool use onto this state.

        Args:
            tool (BaseTool): the tool object to use
            ask_confirmation (bool): whether to ask the user for confirmation before using the tool (default = True)
            confirmation_msg (bool) whether to write a confirmation message the action is about to be taken.

        Returns:
            TState: state object representing the result.

        """
        intent = IntentState(
            circuit_link=self.circuit_link,
            spec=tool.intent(),
            instruction=tool.instruction,
        )
        intent = self.link_to(intent)

        if ask_confirmation and confirmation_msg:
            yes, no = intent.user_confirm()
            no.comment("Inform the user that the action is cancelled in one line.")
            out = yes.comment(
                "Inform the user you are going to take action in one line"
            )

        elif ask_confirmation and not confirmation_msg:
            out, no = intent.user_confirm()
            no.comment("Inform the user that the action is cancelled in one line.")

        else:
            out = intent

        action = UseToolState(
            circuit_link=self.link_to, intent_id=intent.output_id, tool_obj=tool
        )
        return out.link_to(action)

    def intent(self, fmt: IObj, instruction: str = None) -> IntentState:
        """Chain an intent state onto this state. Intent states construct specific json-formatted results defined by a
        format object.

        Args:
            fmt (IObj): the format object constructed with candela.circuits intent
            instruction (str): a system context instruction to inform the json generation process.

        Returns:
            IntentState: the intent state.

        """
        node = IntentState(
            circuit_link=self.circuit_link, spec=fmt, instruction=instruction
        )
        return self.link_to(node)

    def user_confirm(
        self, instruction: Optional[str] = None
    ) -> Tuple[NoOpState, NoOpState]:
        """Add a user confirmation state after this state.

        Args:
            instruction (Optional[str]): optional additional instruction for construction of the confirmation message

        Returns:
            Tuple[NoOpState, NoOpState]: two no op states representing the yes and no choices.

        """
        return ConfirmState.add_user_confirm(self, instruction)

    def user_choice(
        self, *options: str, instruction: Optional[str] = None
    ) -> List[NoOpState]:
        """Add a state that lets the user choose between multiple choices.

        Args:
            *options (str): the options to choose from.
            instruction (Optional[str]):  optional additional instruction for construction of the confirmation message

        Returns:
            List[NoOpState]: a list of no-op states. One representing each user choice.

        """
        return ConfirmState.add_user_choice(
            self, list(options), instruction=instruction
        )

    def add_context(self, **kwargs: str) -> InsertContextState:
        """Add a state that inserts static key-value pairs as system lines. This is a way of adding context for later
        generation.

        Args:
            **kwargs (str): context values to add.

        Returns:
            InsertContextState: the insert context state.

        """
        x = self
        for k, v in kwargs.items():
            x = x.link_to(
                InsertContextState(label=k, context=v, circuit_link=self.circuit_link)
            )
        return x

    def join(self, *others: OpState) -> NoOpState:
        """Join multiple nodes together with a no-op state. This will allow multiple branches to be brought back
        together to a single state. You can then chain another state on.

        Args:
            *others (OpState): the states to join together with this one.

        Returns:
            NoOpState: the no op state representing the join of these states.

        """
        join_node = NoOpState(label="join", circuit_link=self.circuit_link)
        join_node = self.link_to(join_node)
        for other in others:
            join_node = other.link_to(join_node)
        return join_node


class ResponseState(OpState):
    """Class representing a response state in a circuit. Response states are normal chat responses that can optionally
    be constrained to a particular form with a guidance template.

    """

    as_block: StrictBool
    template: Optional[StrictStr]
    context: Optional[StrictStr]
    inserts: Dict[str, str]


class IntentState(OpState):
    """Class representing an intent state. Intent states construct a json with a defined structure that depends on
    prior dialogue content.

    """

    as_block: StrictBool = Field(True)

    spec: Union[IObj, IArr]
    instruction: Optional[StrictStr] = Field(None)


class ConfirmState(OpState):
    """Class representing a user confirmation state."""

    as_block: StrictBool = Field(False)

    instruction: Optional[StrictStr] = Field(None)
    options: List[StrictStr]

    @staticmethod
    def _circuit_and_link(parent: OpState):

        if isinstance(parent, OpState):
            return parent.circuit_link, parent.link_to
        else:
            return parent.link_to, parent.link_to

    @staticmethod
    def add_user_confirm(
        parent: OpState, instruction: str | None = None
    ) -> Tuple[NoOpState, NoOpState]:
        circuit_link, link = ConfirmState._circuit_and_link(parent)

        if instruction is None:
            instruction = "Write a line asking the user to confirm the action."

        confirm = ConfirmState(
            circuit_link=circuit_link, options=["yes", "no"], instruction=instruction
        )
        confirm = link(confirm)

        yes, no, unclear = confirm.switch(
            yes="User has confirmed the request",
            no="User has cancelled the request",
            unclear="User intent is unclear",
        )

        unclear.comment("Briefly state that you don't understand.").link_to(confirm)
        return yes, no

    @staticmethod
    def add_user_choice(
        parent: OpState, options: List[str], instruction: str | None = None
    ) -> List[NoOpState]:
        circuit_link, link = ConfirmState._circuit_and_link(parent)

        if instruction is None:
            instruction = (
                "Strictly ask the user to choose one of these options: ("
                + ", ".join(options)
                + ")"
            )

        confirm = ConfirmState(
            circuit_link=circuit_link, options=options, instruction=instruction
        )
        confirm = link(confirm)
        kwargs = {o: f"user chose {o}" for o in options}
        *cases, unclear = confirm.switch(**kwargs, unclear="User choice is not clear")

        unclear.comment("Briefly state that you don't understand.").link_to(confirm)

        return cases


class NoOpState(OpState):
    """Class representing a no-op op state. This is used to represent cases in switching logic and joining branching
    states back together.

    """

    label: StrictStr
    as_block: StrictBool = Field(False)

    def get_label(self):
        """Get the label of this node type

        Returns:
            str: the node type label string
        """
        return self.label


class UseToolState(OpState):
    """Class representing a tool use state. Tools are bit of code that take intents and perform an action.
    This lets circuits call out to external systems or local software.

    """

    as_block: StrictBool = Field(False)
    intent_id: StrictStr
    tool_obj: BaseTool

    def get_label(self):
        """Get the label of this node type

        Returns:
            str: the node type label string
        """
        return type(self.tool_obj).__name__


class SwitchState(State):
    """Class representing a switch state. Switch states allow conditional branching of states so the circuit can
    branch down multiple paths depending on the prior dialog state.

    """

    case_spec: Dict[str, str]
    case_objs: Dict[str, NoOpState] = Field(default_factory=dict)

    def build_cases(self) -> List[NoOpState]:
        """Build the case no-op states, link them to this state and return them.

        Returns:
            List[NoOpState]: list of no-op states representing the cases

        """
        legs = []
        for k in self.case_spec.keys():
            leg = NoOpState(label=f"case: {k}", circuit_link=self.circuit_link)
            self.circuit_link(leg)
            legs.append(leg)
            self.case_objs[k] = leg
        return legs


class InsertContextState(OpState):
    """A class representing a state that adds some fixed sys context."""

    as_block: StrictBool = Field(False)

    label: StrictStr
    context: StrictStr
