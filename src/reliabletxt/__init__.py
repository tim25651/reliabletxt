# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
from __future__ import annotations

from enum import Enum
from pathlib import Path

from reliabletxt.utils import StrPath, chars_to_ords, ords_to_chars

# class ReliableTxtLines:
#     @staticmethod
#     def split(text: str) -> list[str]:
#         return text.split("\n")

#     @staticmethod
#     def join(lines: list[str]) -> str:
#         return "\n".join(lines)

START_CHAR = "\ufeff"


class ReliableTxtEncoding(Enum):
    """The encoding of a ReliableTXT document

    UTF-8, UTF-16, UTF-16-REVERSE or UTF-32
    """

    UTF_8 = "utf-8"
    UTF_16 = "utf-16-be"
    # UTF_16_REVERSE = "utf-16-le"
    # UTF_32 = "utf-32-be"


class ReliableTxt:
    PREAMBLES = {
        ReliableTxtEncoding.UTF_8: b"\xef\xbb\xbf",
        ReliableTxtEncoding.UTF_16: b"\xfe\xff",
        # ReliableTxtEncoding.UTF_16_REVERSE: b"\xff\xfe",
        # ReliableTxtEncoding.UTF_32: b"\x00\x00\xfe\xff",
    }

    @staticmethod
    def encode(text: str, encoding: ReliableTxtEncoding) -> bytes:
        """Encode a text in the chosen encoding

        Args:
            text (str): The text to encode
            encoding (ReliableTxtEncoding): The encoding to use

        Returns:
            The encoded text
        """
        return text.encode(encoding=encoding.value)

    @classmethod
    def get_encoding(cls, content: bytes) -> ReliableTxtEncoding:
        """Get the encoding of a document with a ReliableTXT preamble.

        Args:
            content (bytes): The content of the document.

        Returns:
            The encoding of the document (utf-8, utf-16).
        """
        for encoding, preamble in cls.PREAMBLES.items():
            if content.startswith(preamble):
                return encoding

        raise ValueError("Document does not have a ReliableTXT preamble")

    @classmethod
    def decode(cls, content: bytes) -> tuple[ReliableTxtEncoding, str]:
        """Decode a document with a ReliableTXT preamble.

        Detects the encoding of the document and decodes it and removes the preamble.

        Args:
            content (bytes): The content of the document.

        Returns:
            The encoding of the document and the text.
        """
        detected_encoding = cls.get_encoding(content)
        encoding = detected_encoding.value
        text = content.decode(encoding=encoding)
        text = text[1:]  # Remove the Preamble
        return detected_encoding, text


class ReliableTxtDocument:
    def __init__(
        self, text: str = "", encoding: ReliableTxtEncoding = ReliableTxtEncoding.UTF_8
    ):
        self._text = text
        self._encoding = encoding

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    @property
    def encoding(self) -> ReliableTxtEncoding:
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: ReliableTxtEncoding) -> None:
        self._encoding = encoding

    @property
    def content(self) -> bytes:
        return ReliableTxt.encode(self._text, self._encoding)

    @property
    def ords(self) -> list[int]:
        return chars_to_ords(self._text)

    @ords.setter
    def ords(self, ords: list[int]) -> None:
        self._text = ords_to_chars(ords)

    def save(self, file_path: StrPath) -> None:
        Path(file_path).write_text(
            "\ufeff" + self._text, encoding=self.encoding.value, newline="\n"
        )

    @staticmethod
    def load(file_path: StrPath) -> ReliableTxtDocument:
        content = Path(file_path).read_bytes()
        encoding, text = ReliableTxt.decode(content)
        return ReliableTxtDocument(text, encoding)


class ReliableTxtCharIterator:
    def __init__(self, text: str):
        self._chars = chars_to_ords(text)
        self._ix = 0

    def get_line_info(self) -> tuple[int, int]:
        line_ix = 0
        line_position = 0
        for i in range(self._ix):
            if self._chars[i] == 0x0A:
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
