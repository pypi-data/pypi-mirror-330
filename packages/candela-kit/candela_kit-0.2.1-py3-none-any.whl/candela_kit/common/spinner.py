from __future__ import annotations

from itertools import cycle
from threading import Thread
from time import sleep, time

from termcolor import colored


class Spinner:
    """A text-based spinner class to signify that something's running and to display progress info."""

    _symbols = [" · ", " ✦ ", " ✶ ", " ✸ ", " ✹ ", " ✺ ", " ✹ ", " ✷ ", " ✦ "]
    _tick = colored(" ✔ ", "green")
    _cross = colored(" ⛌ ", "red")
    _info = colored(" 𝒊 ", "cyan")
    _warn = colored(" ! ", "yellow")
    _interval = 0.1
    _section_colour = "cyan"

    def __init__(
        self,
        message: str = "Working",
        done_message: str | None = None,
        suppress_errors=False,
    ):
        """Constructor for the spinner class

        Args:
            message (str): the message to display while running the spinner
            suppress_errors (bool): whether to catch and suppress errors (default = False)
        """
        self._message = message
        self._suppress_errors = suppress_errors
        self._running = False
        self._start_t = None
        self._prior_line_len = 0
        self._done_text = done_message
        self._thread = Thread(target=self._run, daemon=True)
        self._cycle = cycle([colored(s, "yellow") for s in self._symbols])

    def _clear_chars(self):
        if self._prior_line_len > 0:
            return "\r" + " " * self._prior_line_len + "\r"
        return ""

    def _print(self, symbol: str, msg: str | None, end: str, show_time: bool = True):

        wipe = self._clear_chars()

        if msg is None:
            print(wipe, end="", flush=True)
            return

        time_str = f" ({time() - self._start_t:2.1f}s)" if show_time else ""
        line_parts = [wipe, symbol, msg, time_str]

        line = "".join(line_parts)
        print(line, flush=True, end=end)
        self._prior_line_len = len(line) - len(wipe)

    def _run(self):
        self._start_t = time()
        while self._running:
            sleep(self._interval)
            self._print(next(self._cycle), self._message, end="")

    @property
    def message(self):
        """Getter for the spinner message"""
        return self._message

    @message.setter
    def message(self, text: str):
        """Setter for the spinner message"""
        self._message = text

    def section(self, msg: str):
        """Print a section heading"""
        wipe = self._clear_chars()
        print(wipe + "[" + colored(msg, self._section_colour) + "]")
        self._prior_line_len = 0

    def info(self, msg: str):
        """Print an info message. This will print a message on a line and then continue the spinner underneath.

        Args:
            msg (str): the info message

        """
        self._print(self._info, msg, "\n")

    def warn(self, msg: str):
        """Print a warning message. This will print a message on a line and then continue the spinner underneath.

        Args:
            msg (str): the warning message

        """
        self._print(self._warn, msg, "\n")

    @property
    def done(self) -> str | None:
        return self._done_text

    @done.setter
    def done(self, text: str):
        self._done_text = text

    def __enter__(self) -> Spinner:
        self._running = True
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._running = False
        self._thread.join()

        if exc_type is None:
            end = "\n" if self.done is not None else ""
            self._print(self._tick, self.done, end)
            return False
        else:
            self._print(self._cross, f"{exc_type.__name__}: {exc_val}", "\n")
            return self._suppress_errors
