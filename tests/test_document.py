"""Tests for the ReliableTxtDocument class and the encode/decode functions."""

from __future__ import annotations

from pathlib import Path

import pytest
from reliabletxt import ReliableTxtDocument, decode, encode

ASSETS = Path(__file__).parent / "assets"

TABLE = (
    'a \tU+0061    61            0061        "Latin Small Letter A"\n'
    "~ \tU+007E    7E            007E        Tilde\n"
    '¥ \tU+00A5    C2_A5         00A5        "Yen Sign"\n'
    '» \tU+00BB    C2_BB         00BB        "Right-Pointing Double Angle Quotation Mark"\n'
    '½ \tU+00BD    C2_BD         00BD        "Vulgar Fraction One Half"\n'
    '¿ \tU+00BF    C2_BF         00BF        "Inverted Question Mark"\n'
    'ß \tU+00DF    C3_9F         00DF        "Latin Small Letter Sharp S"\n'
    'ä \tU+00E4    C3_A4         00E4        "Latin Small Letter A with Diaeresis"\n'
    'ï \tU+00EF    C3_AF         00EF        "Latin Small Letter I with Diaeresis"\n'
    'œ \tU+0153    C5_93         0153        "Latin Small Ligature Oe"\n'
    '€ \tU+20AC    E2_82_AC      20AC        "Euro Sign"\n'
    '東 \tU+6771    E6_9D_B1      6771        "CJK Unified Ideograph-6771"\n'
    '𝄞 \tU+1D11E   F0_9D_84_9E   D834_DD1E   "Musical Symbol G Clef"\n'
    '𠀇 \tU+20007   F0_A0_80_87   D840_DC07   "CJK Unified Ideograph-20007"'
)


def test_decode_strips_bom() -> None:
    with_bom = decode((ASSETS / "Example01_Table_UTF8.txt").read_bytes())
    without_bom = decode((ASSETS / "Example08_Table_UTF8_NoBOM.txt").read_bytes())
    assert with_bom == without_bom == TABLE


def test_decode_empty() -> None:
    assert decode((ASSETS / "Example02_Empty_UTF8.txt").read_bytes()) == ""


def test_decode_four_lines() -> None:
    text = decode((ASSETS / "Example03_FourLines_UTF8.txt").read_bytes())
    assert text == "Line 1\nLine 2\nLine 3\n"


def test_decode_long_lines() -> None:
    text = decode((ASSETS / "Example04_LongLines_UTF8.txt").read_bytes())
    expected = "\n".join("".join(f"LongLine{char}_{ix:03d}" for ix in range(1000)) for char in "AB")
    assert text == expected


def test_decode_c0() -> None:
    text = decode((ASSETS / "Example05_C0_UTF8.txt").read_bytes())
    assert text == "".join(chr(i) for i in range(32))


def test_decode_unicode_line_breaks() -> None:
    text = decode((ASSETS / "Example06_UnicodeLineBreaks_UTF8.txt").read_bytes())
    assert len(text.split("\n")) == 3


def test_decode_cjk() -> None:
    text = decode((ASSETS / "Example07_CJK_UTF8.txt").read_bytes())
    assert text == "".join(chr(i) for i in range(0x4E00, 0x4E00 + 100))


def test_decode_corrupt_data_raises() -> None:
    content = (ASSETS / "InvalidExample02_CorruptData_UTF8.txt").read_bytes()
    with pytest.raises(UnicodeDecodeError):
        decode(content)


def test_encode_roundtrip() -> None:
    assert decode(encode(TABLE)) == TABLE


def test_document_defaults_to_writable() -> None:
    document = ReliableTxtDocument("a")
    document.text = "b"
    assert document.text == "b"


def test_document_read_only_rejects_write() -> None:
    document = ReliableTxtDocument("a", read_only=True)
    with pytest.raises(ValueError, match="read-only"):
        document.text = "b"


def test_document_content_is_utf8_without_bom() -> None:
    assert ReliableTxtDocument("a").content == b"a"


def test_document_save_load_roundtrip(tmp_path: Path) -> None:
    file_path = tmp_path / "doc.txt"
    ReliableTxtDocument(TABLE).save(file_path)
    loaded = ReliableTxtDocument.load(file_path)
    assert loaded.text == TABLE
    assert not loaded.read_only


def test_document_save_omits_bom(tmp_path: Path) -> None:
    file_path = tmp_path / "doc.txt"
    ReliableTxtDocument("a").save(file_path)
    assert file_path.read_bytes() == b"a"
