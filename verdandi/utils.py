import os
import shutil
from typing import Any, List


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
