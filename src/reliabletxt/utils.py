"""Utility functions for reliabletxt"""

from os import PathLike
from pathlib import Path
from typing import TypeAlias

StrPath: TypeAlias = str | PathLike[str] | Path


def chars_to_ords(chars: str) -> list[int]:
    """Convert a string to a list of code points

    Args:
        chars (str): The string to convert

    Returns:
        The list of code points
    """
    return [ord(c) for c in chars]


def ords_to_chars(ords: list[int]) -> str:
    """Convert a list of code points to a string

    Args:
        ords (list[int]): The list of code points to convert

    Returns:
        the joined string
    """
    return "".join([chr(c) for c in ords])
