import io
import json
from abc import ABC, abstractmethod
from collections.abc import Sized
from contextlib import nullcontext
from time import sleep
from typing import Iterator, Literal, Iterable, Tuple

from pandas import read_csv
from tabulate import tabulate
from termcolor import colored

from ..client import Client
from ..common.common import labelled_msg, indent_str
from ..common.spinner import Spinner
from ..dtos import ObjectId, Event, ObjectMetadata, SlotState, ToolModule

MAX_LEN = 80


def intent_print(evt, skip=False):
    if skip:
        return
    chunk = evt.content.replace("\n", "\n    ")
    print(colored(chunk, "green"), end="", flush=True)


def info_print(evt, skip=False):
    if skip:
        return
    labelled_msg("INFO", evt.content, "cyan")


def wait_print(evt, skip=False):
    if skip:
        return
    labelled_msg("WAIT", evt.content, "magenta")


def sys_print(evt, skip=False):
    if skip:
        return
    labelled_msg("SYS", evt.content, "light_grey")


def result_print(evt):
    d = json.loads(evt.content)

    labelled_msg("RESULT", d["content_type"], "green")

    if d["content_type"] == "table":
        df = read_csv(io.StringIO(d["content"]["data"]))
        content_str = tabulate(df, headers=df.columns, tablefmt="rounded_outline")
    else:
        content_str = json.dumps(d["content"], indent=2)

    print(indent_str(content_str, n=4))


class SessionContext(ABC):

    def __init__(
        self,
        client: Client,
        slot_type: str,
        model_id: ObjectId,
        tool_module_override: ToolModule,
    ):
        self.client = client
        self.slot_type = slot_type
        self.model_id = model_id
        self.tool_module_override = tool_module_override
        self.session_meta = None

    @abstractmethod
    def _start_session(self) -> ObjectMetadata:
        raise NotImplementedError()

    def __enter__(self):
        with Spinner("Assigning slot") as spinner:
            spinner.section(f"Starting {type(self).__name__} context")

            if not self.client.has_slot():
                self.client.assign_slot(self.slot_type)

            meta = self.client.get_slot_metadata()
            spinner.info(f"User assigned to slot {meta.slot_id}")

            state = self.client.get_slot_state()
            while state != SlotState.HOST_READY:
                spinner.message = (
                    f"Waiting for {meta.slot_id} to be ready (status = {state.name})"
                )
                sleep(1)
                state = self.client.get_slot_state()
            spinner.done = "Slot is ready"

        with Spinner("Starting session") as spinner:
            self.client.stop_session()
            self.session_meta = self._start_session()
            spinner.done = f"Session {self.session_meta.obj_id.identifier} is ready"

        print()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # stop session
        self.client.stop_session()


class RunAgent(SessionContext, ABC):

    def _submit_prompt(self, prompt: str):
        return self.client.submit_prompt_to_agent(
            prompt, self.session_meta.obj_id.identifier
        )

    @staticmethod
    def _user_stream_handler(stream: Iterator[Event]) -> Event | None:
        print("\n" + colored("Assistant", "blue") + ":")
        return next(stream, None)

    @staticmethod
    def _chunk_wrapper(evt: Event, line_len: int) -> Tuple[str, int]:

        if line_len == 0:
            evt.content = "  " + evt.content.lstrip()
        chunk = evt.content.replace("\n", "\n  ")

        if "\n" in chunk:
            line_len = len(chunk.split("\n")[-1])
        else:
            line_len += len(chunk)

        if line_len > MAX_LEN:

            parts = chunk.split(" ")

            to_join = [parts[0], "\n "]
            if len(parts) > 1:
                to_join += parts[1:]
            chunk = " ".join(to_join)

            line_len = len(chunk) - len(parts[0]) - 1

        return chunk, line_len

    @staticmethod
    def _chat_stream_handler(evt, stream: Iterator[Event]) -> Event | None:

        while evt and evt.content.strip() == "":
            evt = next(stream, None)

        line_len = 0
        while evt is not None and evt.event_type == "chat":
            chunk, line_len = RunAgent._chunk_wrapper(evt, line_len)
            print(chunk, end="", flush=True)
            evt = next(stream, None)

        print()
        return evt

    @staticmethod
    def _intent_stream_handler(
        evt, stream: Iterator[Event], mode: Literal["quiet", "debug", "developer"]
    ) -> Event | None:

        verbose = mode != "quiet"
        context = nullcontext() if verbose else Spinner("Thinking")

        evt.content = evt.content.lstrip()

        if verbose:
            print(f'  [{colored("INTENT", "green")}]:')
            print("    ", end="")

        with context:
            while evt is not None and evt.event_type == "intent":
                intent_print(evt, not verbose)
                evt = next(stream, None)
        print()
        return evt

    @staticmethod
    def _wait_stream_handler(
        evt, stream: Iterator[Event], mode: Literal["quiet", "debug", "developer"]
    ) -> Event | None:

        verbose = mode == "developer"
        context = nullcontext() if verbose else Spinner("Using tool")

        with context:
            while evt is not None and evt.event_type == "wait":
                wait_print(evt, not verbose)
                evt = next(stream, None)
        return evt

    @staticmethod
    def _sys_stream_handler(
        evt, stream: Iterator[Event], mode: Literal["quiet", "debug", "developer"]
    ) -> Event | None:
        sys_print(evt, mode != "developer")
        return next(stream, None)

    @staticmethod
    def _info_stream_handler(
        evt, stream: Iterator[Event], mode: Literal["quiet", "debug", "developer"]
    ) -> Event | None:
        show_lines = mode == "developer"

        context = nullcontext() if show_lines else Spinner("Thinking")
        with context:
            while evt is not None and evt.event_type == "info":
                info_print(evt, skip=not show_lines)
                evt = next(stream, None)
        return evt

    @staticmethod
    def _result_stream_handler(evt, stream: Iterator[Event]) -> Event | None:
        result_print(evt)
        return next(stream, None)

    def chat(self, mode: Literal["quiet", "debug", "developer"] = "developer"):

        handlers = {
            "chat": lambda e, s, m: RunAgent._chat_stream_handler(e, s),
            "intent": RunAgent._intent_stream_handler,
            "wait": RunAgent._wait_stream_handler,
            "sys": RunAgent._sys_stream_handler,
            "info": RunAgent._info_stream_handler,
            "result": lambda e, s, m: RunAgent._result_stream_handler(e, s),
            "user": lambda e, s, m: RunAgent._user_stream_handler(s),
        }

        while True:
            print(colored("User", "blue") + ":")
            message = input("  ")
            if message == "quit()":
                print("  User quit the chat session")
                self.client.stop_session()
                return

            stream = self._submit_prompt(message)

            evt = next(stream)
            while evt:
                evt = handlers[evt.event_type](evt, stream, mode)


class RunPipeline(SessionContext, ABC):

    def _submit_prompt(self, prompt: str):
        return self.client.submit_prompt_to_pipeline(
            prompt, self.session_meta.obj_id.identifier
        )

    def call(self, prompt, ix=None, total=None):

        msg = "Pipeline is processing prompt"
        if ix is not None:
            msg += f" ({ix}"
        if total is not None:
            msg += f"/{total})"
        elif ix is not None:
            msg += ")"

        with Spinner(msg) as spinner:
            res = self._submit_prompt(prompt)
            spinner.done = f"Prompt processed ({res['metadata']['request_id']})"
        return res

    def map(self, prompts: Iterable[str]) -> Iterable[dict]:
        total = None
        if isinstance(prompts, Sized):
            total = len(prompts)

        for i, prompt in enumerate(prompts):
            yield self.call(prompt, i + 1, total)


class RunAgentApp(RunAgent):

    def __init__(self, client, slot_type, model_id, app_id, tool_module_override):
        self.app_id = app_id
        super().__init__(client, slot_type, model_id, tool_module_override)

    def _start_session(self) -> ObjectMetadata:
        sess = self.client.start_session(self.app_id, self.model_id)
        return sess


class RunPipelineApp(RunPipeline):

    def __init__(self, client, slot_type, model_id, app_id, tool_module_override):
        self.app_id = app_id
        super().__init__(client, slot_type, model_id, tool_module_override)

    def _start_session(self) -> ObjectMetadata:
        sess = self.client.start_session(self.app_id, self.model_id)
        return sess


class RunAgentCircuit(RunAgent):

    def __init__(
        self, client, slot_type, model_id, directive, circuit, tool_module_override
    ):
        self.directive = directive
        self.circuit = circuit
        super().__init__(client, slot_type, model_id, tool_module_override)

    def _start_session(self) -> ObjectMetadata:
        return self.client.start_dev_session(
            self.circuit,
            self.directive,
            self.model_id,
            tool_module_override=self.tool_module_override,
        )


class RunPipelineCircuit(RunPipeline):

    def __init__(
        self, client, slot_type, model_id, directive, circuit, tool_module_override
    ):
        self.directive = directive
        self.circuit = circuit
        super().__init__(client, slot_type, model_id, tool_module_override)

    def _start_session(self) -> ObjectMetadata:
        return self.client.start_dev_session(
            self.circuit,
            self.directive,
            self.model_id,
            tool_module_override=self.tool_module_override,
        )
