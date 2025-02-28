from __future__ import annotations

from typing import List, Optional, Dict, Type
from typing import Tuple, Union

from graphviz import Digraph
from pydantic import BaseModel, StrictStr, Field

from .states import (
    ResponseState,
    IntentState,
    ConfirmState,
    UseToolState,
    SwitchState,
    InsertContextState,
    NoOpState,
    State,
    TState,
    OpState,
)
from ..ignite.intent import IObj
from ..tools.base import BaseTool


class Circuit(BaseModel):
    """A class that represents a flow of states (circuits) that constitutes the control flow logic of an agent or
    pipeline.

    """

    first: Optional[StrictStr] = None
    current: Optional[StrictStr] = None
    nodes: dict[
        str,
        Union[
            ResponseState,
            IntentState,
            ConfirmState,
            UseToolState,
            SwitchState,
            InsertContextState,
            NoOpState,
        ],
    ] = Field(default_factory=dict)

    def get_tool_classes(self) -> List[Type[BaseTool]]:
        nodes = self.nodes.values()
        tool_classes = [
            type(node.tool_obj) for node in nodes if isinstance(node, UseToolState)
        ]
        return [t for t in tool_classes if issubclass(t, BaseTool)]

    def _callable_once(self):
        if self.first is not None:
            raise ValueError(
                f"Circuit already has a start node: {type(self.nodes[self.first]).__name__} {self.first}"
            )

    def link_to(self, node: TState) -> TState:
        """Link a state to this circuit.

        Args:
            node (TState): the state to link.

        Returns:
            TState: the linked state.

        """
        if self.first is None:
            self.first = node.node_id
        self.nodes[node.node_id] = node
        return node

    def switch(self, **kwargs: str) -> List[NoOpState]:
        """Switch between some given cases. This is for introducing branching logic in the circuits.

        Args:
            **kwargs (str): the individual cases to branch down. The keyword is the name of the case and the string
            input is the condition associated with the case.

        Returns:
            List[NoOpState]: a list of no-op states that represent the different cases of the switch.

        """
        self._callable_once()
        cdn = SwitchState(circuit_link=self.link_to, case_spec=kwargs)
        return self.link_to(cdn).build_cases()

    def comment(
        self, msg: Optional[str] = None, template: Optional[str] = None, **inserts
    ) -> ResponseState:
        """Chain a comment state as the first state of the circuit.

        Args:
            msg (Optional[str]): context message to form the response.
            template (Optional[str]): template to constrain the response.
            **inserts (Optional[Join | Select]): guidance objects to insert into the template.

        Returns:
            ResponseState: the response state representing the comment.

        """
        self._callable_once()
        inserts = {k: str(v) for k, v in inserts.items()}
        comment = ResponseState(
            circuit_link=self.link_to,
            context=msg,
            template=template,
            as_block=False,
            inserts=inserts,
        )
        return self.link_to(comment)

    def intent(self, fmt: IObj, instruction: Optional[str] = None) -> IntentState:
        """Chain an intent state as the first state of the circuit. Intent states construct specific json-formatted
        results defined by a format object.

        Args:
            fmt (IObj): the format object constructed with candela.circuits intent
            instruction (str): a system context instruction to inform the json generation process.

        Returns:
            IntentState: the intent state.

        """
        self._callable_once()
        node = IntentState(circuit_link=self.link_to, spec=fmt, instruction=instruction)
        return self.link_to(node)

    def user_confirm(
        self, instruction: Optional[str] = None
    ) -> Tuple[NoOpState, NoOpState]:
        """Add a user confirmation state as the first state of the circuit.

        Args:
            instruction (Optional[str]): optional additional instruction for construction of the confirmation message

        Returns:
            Tuple[NoOpState, NoOpState]: two no op states representing the yes and no choices.

        """
        self._callable_once()
        return ConfirmState.add_user_confirm(self, instruction)

    def user_choice(
        self, *options: str, instruction: Optional[str] = None
    ) -> List[NoOpState]:
        """Add a state that lets the user choose between multiple choices as the first state of the circuit.

        Args:
            *options (str): the options to choose from.
            instruction (Optional[str]):  optional additional instruction for construction of the confirmation message

        Returns:
            List[NoOpState]: a list of no-op states. One representing each user choice.

        """
        self._callable_once()
        return ConfirmState.add_user_choice(
            self, list(options), instruction=instruction
        )

    def add_context(self, **kwargs: str) -> InsertContextState:
        """Add a state that inserts static key-value pairs as system lines as the first state of the circuit.
        This is a way of adding context for later generation.

        Args:
            **kwargs (str): context values to add.

        Returns:
            InsertContextState: the insert context state.

        """
        self._callable_once()
        x = self
        for k, v in kwargs.items():
            x = x.link_to(
                InsertContextState(label=k, context=v, circuit_link=self.link_to)
            )
        return x

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
        self._callable_once()
        intent = IntentState(
            circuit_link=self.link_to, spec=tool.intent(), instruction=tool.instruction
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

    @staticmethod
    def _add_op_state_to_digraph(dot: Digraph, state: OpState):
        if state.child_id is None:
            dot.node(state.node_id, state.get_label() + f"\n[{state.node_id}]")
            # no edge from this node
            return

        dot.edge(state.node_id, state.child_id)

    @staticmethod
    def _add_switch_to_digraph(dot: Digraph, state: SwitchState):
        for v in state.case_objs.values():
            dot.edge(state.node_id, v.node_id)

    def _get_digraph_with_nodes(self) -> Digraph:
        dot = Digraph()

        dot.node("input", "user\nprompt")

        for node_id, node in self.nodes.items():
            label = node.get_label()
            dot.node(node_id, label)

        dot.edge("input", self.first)
        dot.attr(rankdir="TB")
        return dot

    def get_digraph(self) -> Digraph:

        dot = self._get_digraph_with_nodes()

        for i, state in enumerate(self.nodes.values()):

            if isinstance(state, OpState):
                self._add_op_state_to_digraph(dot, state)
            elif isinstance(state, SwitchState):
                self._add_switch_to_digraph(dot, state)
            else:
                raise TypeError(f"Unsupported node type: {type(state).__name__}")

        return dot

    def _repr_mimebundle_(self, *args, **kwargs):
        dot = self.get_digraph()
        return dot._repr_mimebundle_(*args, **kwargs)

    def get_end_states(self) -> Dict[str, State]:
        """Get a dictionary of end states of this circuit.

        The end states are states with no children in the underlying graph.
        They are where one iteration through the circuit finishes.

        Returns:
            Dict[str, State]: dictionary of states where keys are node id strings.

        """
        end_state_nodes = {}
        for node_id, node in self.nodes.items():
            if not isinstance(node, SwitchState) and node.child_id is None:
                node = node.model_copy(update={"circuit_link": self.link_to})
                end_state_nodes[node_id] = node
                self.nodes[node_id] = node

        return end_state_nodes


Circuit.model_rebuild()


def circuit() -> Circuit:
    """Create an empty circuit object

    Returns:
        Circuit: the new circuit object
    """
    return Circuit()
