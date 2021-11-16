from __future__ import annotations

import os
import shutil
import sys
from collections import UserList
from contextlib import ContextDecorator
from io import StringIO
from typing import Any, List


class StreamCapture(ContextDecorator, UserList):
    """
    Context manager that replaces the standard output with StringIO buffer
    and keeps the output in a list
    """

    def __enter__(self) -> StreamCapture:
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def make_name_importable(name: str) -> str:
    """
    Converts a system path to importable name
    """
    if os.path.isfile(name) and name.lower().endswith(".py"):
        name = name[:-3].replace("./", "").replace("\\", ".").replace("/", ".")
        while name.startswith("."):
            name = name[1:]
        return name
    return name


def flatten(deep_list: List[Any]) -> List[Any]:
    """
    Recursively flatten the list into 1D list containing all nested elements
    """
    if len(deep_list) == 0:
        return deep_list
    if isinstance(deep_list[0], list):
        return flatten(deep_list[0]) + flatten(deep_list[1:])
    return deep_list[:1] + flatten(deep_list[1:])


def print_header(text: str, padding_symbol: str = "=") -> None:
    """
    Prints given text padded from both sides with `padding_symbol` up to terminal width
    """
    text_length = len(text)
    columns = shutil.get_terminal_size()[0]

    padding_length = ((columns - text_length) // 2) - 1  # Substract one whitespace from each side
    padding = padding_symbol * padding_length

    print(f"{padding} {text} {padding}")
