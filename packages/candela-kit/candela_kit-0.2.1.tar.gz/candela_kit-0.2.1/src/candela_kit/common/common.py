from __future__ import annotations

import re
from pathlib import Path

import yaml
from pydantic import SecretStr
from termcolor import colored
from tabulate import tabulate
from pyfiglet import figlet_format

n_indent = 4
indent = " " * n_indent


def labelled_msg(label, msg, colour):
    label = f"  [{colored(label, colour)}]"
    msg = colored(msg, colour)
    print(f"{label}: {msg}")


def to_snake_case(camel_case_str: str) -> str:
    """
    Convert a camel case string to a snake case string

    Args:
        camel_case_str (str): input camel case string

    Returns:
        str: generated snake case string
    """
    a = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
    cleaned_str = "".join(camel_case_str.split())
    snake_case = a.sub(r"_\1", cleaned_str).lower()
    return snake_case.replace("__", "_")


def indent_str(s: str, n: int = n_indent) -> str:
    """
    Generate a string that's indented by some number of spaces.

    Args:
        s (str): the input string. Can be a multiline string (contains '\n').
        n (int): in number of spaces to indent. Defaults to 4.

    Returns:
        str: the indented version of the string.

    """
    _indent = " " * n
    return "\n".join(map(lambda x: f"{_indent}{x}", s.split("\n")))


def print_subtitle(title: str, n: int = 2):
    print(" " * n + colored(title, "cyan") + ":")


def print_table(df, title=None, n=2, max_col_width=48):

    df = df.copy()
    table_indent = n

    if title is not None:
        print_subtitle(title, n)
        table_indent += 2

    if df.shape[0] == 0:
        print(indent_str("[Nothing to display]", table_indent))
    else:
        df = df.fillna("[Not Available]")
        for c in df.columns:
            df[c] = df[c].astype(str).str.wrap(max_col_width)

        cols = [colored(c, "green").replace("_", " ") for c in df.columns]
        table_str = tabulate(df, cols, tablefmt="rounded_grid")
        table_str = indent_str(table_str, table_indent)
        print(table_str)
    print()


def print_line(max_len=68):
    print(colored("-" * max_len))


def print_title(title, **metadata):
    title = figlet_format(title, font="slant")
    print_line()
    print(colored(title, "cyan"), end="")
    print_line()
    names = metadata.keys()
    max_len = max([len(n) for n in names])
    for name in names:
        k = colored(name, "cyan")
        extra = " " * (max_len - len(name))
        print(f"    {extra}{k}: {metadata[name]}")
    print_line()


CANDELA_DIR = Path.home() / ".candela"


class CustomDumper(yaml.Dumper):

    def _path(self, data):
        return super().represent_data(str(data))

    def _secrets_str(self, data):
        val = data.get_secret_value()

        if val == "local":
            return super().represent_data("local")

        return super().represent_data(val[:3] + "*" * 16 + val[-5:])

    def represent_data(self, data):
        if isinstance(data, Path):
            return self._path(data)
        elif isinstance(data, SecretStr):
            return self._secrets_str(data)
        else:
            return super().represent_data(data)


def print_model(d, title: str = None, n: int = 2):

    dict_indent = n

    if title is not None:
        print_subtitle(title, n)
        dict_indent += 2

    d_str = yaml.dump(d.model_dump(), Dumper=CustomDumper)

    d_str = d_str.rstrip()

    print(indent_str(d_str, dict_indent))
    print()
