import os


def convert_name(name: str) -> str:
    """
    Converts a system path to importable name
    """
    if os.path.isfile(name) and name.lower().endswith(".py"):
        return name[:-3].replace("./", "").replace("\\", ".").replace("/", ".")
    return name
