from _typeshed import StrPath

def encode(text: str) -> bytes:
    """Encodes text as UTF-8 bytes."""

def decode(content: bytes) -> str:
    """Decodes UTF-8 bytes into text, stripping a leading BOM if present.

    Raises:
        UnicodeDecodeError: If content is not valid UTF-8.
    """

class ReliableTxtDocument:
    """Manages the text content of a ReliableTXT document."""

    def __init__(self, text: str = "", read_only: bool = False) -> None: ...
    @property
    def read_only(self) -> bool:
        """Whether the text of the document can be reassigned."""

    @property
    def text(self) -> str:
        """Current text content of the document."""

    @text.setter
    def text(self, text: str) -> None:
        """Sets text.

        Raises:
            ValueError: If the document is read-only.
        """

    @property
    def content(self) -> bytes:
        """Text content encoded as UTF-8 bytes."""

    def save(self, file_path: StrPath) -> None:
        """Writes the text as UTF-8 to file_path, without a BOM."""

    @staticmethod
    def load(file_path: StrPath) -> ReliableTxtDocument:
        """Loads a document from file_path, stripping a leading BOM if present.

        Raises:
            UnicodeDecodeError: If the file content is not valid UTF-8.
        """

class ReliableTxtCharIterator:
    """Manages a cursor position while walking the characters of a ReliableTXT document."""

    def __init__(self, text: str) -> None: ...
    @property
    def ix(self) -> int:
        """Current cursor position, as a character index into the text."""

    def forward(self) -> None:
        """Advances the cursor by one character."""

    def get_line_info(self) -> tuple[int, int]:
        """Returns the zero-based line index and column of the cursor."""

    def is_eof(self) -> bool:
        """Whether the cursor is at the end of the text."""

    def is_char(self, c: str) -> bool:
        """Whether the character at the cursor is c."""

    def try_read_char(self, c: str) -> bool:
        """Whether the character at the cursor is c, advancing the cursor if so."""
