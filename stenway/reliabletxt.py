# pylint: disable=invalid-name, missing-function-docstring, missing-module-docstring, redefined-builtin, missing-class-docstring
from __future__ import annotations

from enum import Enum


class ReliableTxtLines:
    @staticmethod
    def split(text: str) -> list[str]:
        return text.split("\n")

    @staticmethod
    def join(lines: list[str]) -> str:
        return "\n".join(lines)


class ReliableTxtEncoding(Enum):
    UTF_8 = "utf-8"
    UTF_16 = "utf-16-be"
    UTF_16_REVERSE = "utf-16-le"
    UTF_32 = "utf-32-be"


class ReliableTxtEncoder:
    @staticmethod
    def encode(text: str, encoding: ReliableTxtEncoding) -> bytes:
        encodingName = encoding.value
        return text.encode(encoding=encodingName)


class ReliableTxtDecoder:
    @staticmethod
    def getEncoding(bytes: bytes) -> ReliableTxtEncoding:
        if (
            len(bytes) >= 3
            and bytes[0] == 0xEF
            and bytes[1] == 0xBB
            and bytes[2] == 0xBF
        ):
            return ReliableTxtEncoding.UTF_8

        if len(bytes) >= 2 and bytes[0] == 0xFE and bytes[1] == 0xFF:
            return ReliableTxtEncoding.UTF_16

        if len(bytes) >= 2 and bytes[0] == 0xFF and bytes[1] == 0xFE:
            return ReliableTxtEncoding.UTF_16_REVERSE

        if (
            len(bytes) >= 4
            and bytes[0] == 0
            and bytes[1] == 0
            and bytes[2] == 0xFE
            and bytes[3] == 0xFF
        ):
            return ReliableTxtEncoding.UTF_32

        raise ValueError("Document does not have a ReliableTXT preamble")

    @staticmethod
    def decode(bytes: bytes) -> tuple[ReliableTxtEncoding, str]:
        detectedEncoding = ReliableTxtDecoder.getEncoding(bytes)
        encodingName = detectedEncoding.value
        text = bytes.decode(encoding=encodingName)
        text = text[1:]
        return detectedEncoding, text


class ReliableTxtDocument:
    def __init__(
        self, text: str = "", encoding: ReliableTxtEncoding = ReliableTxtEncoding.UTF_8
    ):
        self._text = text
        self._encoding = encoding

    def setEncoding(self, encoding: ReliableTxtEncoding) -> None:
        self._encoding = encoding

    def setText(self, text: str) -> None:
        self._text = text

    def getEncoding(self) -> ReliableTxtEncoding:
        return self._encoding

    def getText(self) -> str:
        return self._text

    def getBytes(self) -> bytes:
        return ReliableTxtEncoder.encode(self._text, self._encoding)

    def getCodePoints(self) -> list[int]:
        return StringUtil.getCodePoints(self._text)

    def setCodePoints(self, codePoints: list[int]) -> None:
        self._text = StringUtil.fromCodePoints(codePoints)

    def save(self, filePath: str) -> None:
        encodingName = self._encoding.value

        with open(filePath, "w", encoding=encodingName, newline="\n") as file:
            file.write("\ufeff")
            file.write(self._text)

    @staticmethod
    def load(filePath: str) -> ReliableTxtDocument:
        bytes = None
        with open(filePath, "rb") as file:
            bytes = file.read()
        encoding, text = ReliableTxtDecoder.decode(bytes)
        return ReliableTxtDocument(text, encoding)


class StringUtil:
    @staticmethod
    def getCodePoints(text: str) -> list[int]:
        return [ord(c) for c in text]

    @staticmethod
    def fromCodePoints(codePoints: list[int]) -> str:
        chars = [chr(c) for c in codePoints]
        return "".join(chars)


class ReliableTxtCharIterator:
    def __init__(self, text: str):
        self._chars = StringUtil.getCodePoints(text)
        self._index = 0

    def getLineInfo(self) -> tuple[int, int]:
        lineIndex = 0
        linePosition = 0
        for i in range(self._index):
            if self._chars[i] == 0x0A:
                lineIndex += 1
                linePosition = 0
            else:
                linePosition += 1
        return lineIndex, linePosition

    def isEndOfText(self) -> bool:
        return self._index >= len(self._chars)

    def isChar(self, c: int) -> bool:
        if self.isEndOfText():
            return False
        return self._chars[self._index] == c

    def tryReadChar(self, c: int) -> bool:
        if not self.isChar(c):
            return False
        self._index += 1
        return True
