# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
from __future__ import annotations

from enum import Enum
from os import PathLike
from pathlib import Path
from typing import Final, TypeAlias

StrPath: TypeAlias = str | PathLike[str] | Path

NEW_LINE: Final[int] = 0x0A


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


class ReliableTxt:

    @staticmethod
    def encode(text: str) -> bytes:
        """Encode a text with "utf-8" encoding.

        Args:
            text (str): The text to encode
        Returns:
            The encoded text
        """
        return text.encode(encoding="utf-8")

    @classmethod
    def decode(cls, content: bytes) -> str:
        """Decode a document with "utf-8" encoding and adds the BOM.

        Returns:
            The text.
        """
        text = content.decode(encoding="utf-8")
        if text[0] != "\ufeff":
            raise ValueError("The document is not a ReliableTXT document")
        return text[1:]


class ReliableTxtDocument:
    def __init__(self, text: str = "", read_only: bool = False):
        self._text = text
        self._read_only = read_only

    @property
    def read_only(self) -> bool:
        return self._read_only

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        if self._read_only:
            raise ValueError("The document is read-only")

        self._text = text

    @property
    def content(self) -> bytes:
        return ReliableTxt.encode(self._text)

    @property
    def ords(self) -> list[int]:
        return chars_to_ords(self._text)

    @ords.setter
    def ords(self, ords: list[int]) -> None:
        self._text = ords_to_chars(ords)

    def save(self, file_path: StrPath) -> None:
        """Writes the text with the BOM to a file."""
        Path(file_path).write_text(
            "\ufeff" + self._text, encoding="utf-8", newline="\n"
        )

    @staticmethod
    def load(file_path: StrPath) -> ReliableTxtDocument:
        content = Path(file_path).read_bytes()
        text = ReliableTxt.decode(content)
        return ReliableTxtDocument(text)


class ReliableTxtCharIterator:
    def __init__(self, text: str):
        self._chars = chars_to_ords(text)
        self._ix = 0

    def get_line_info(self) -> tuple[int, int]:
        line_ix = 0
        line_position = 0
        for i in range(self._ix):
            if self._chars[i] == NEW_LINE:
                line_ix += 1
                line_position = 0
            else:
                line_position += 1
        return line_ix, line_position

    def is_eof(self) -> bool:
        return self._ix >= len(self._chars)

    def is_char(self, c: int) -> bool:
        if self.is_eof():
            return False
        return self._chars[self._ix] == c

    def try_read_char(self, c: int) -> bool:
        if not self.is_char(c):
            return False
        self._ix += 1
        return True
