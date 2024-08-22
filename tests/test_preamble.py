# %%
from pathlib import Path

import pytest

from reliabletxt import ReliableTxt

# we have the test files in in Path(__file__).parent / "assets" folder.
# read them and decode them

ASSETS = Path(__file__).parent / "assets"
TEST_FILES = {
    "".join(file.stem.replace("_UTF8", "").split("_")[1:]): str(file)
    for file in ASSETS.iterdir()
}


def read(name: str) -> bytes:
    return Path(TEST_FILES[name]).read_bytes()


table = '''a 	U+0061    61            0061        "Latin Small Letter A"
~ 	U+007E    7E            007E        Tilde
¥ 	U+00A5    C2_A5         00A5        "Yen Sign"
» 	U+00BB    C2_BB         00BB        "Right-Pointing Double Angle Quotation Mark"
½ 	U+00BD    C2_BD         00BD        "Vulgar Fraction One Half"
¿ 	U+00BF    C2_BF         00BF        "Inverted Question Mark"
ß 	U+00DF    C3_9F         00DF        "Latin Small Letter Sharp S"
ä 	U+00E4    C3_A4         00E4        "Latin Small Letter A with Diaeresis"
ï 	U+00EF    C3_AF         00EF        "Latin Small Letter I with Diaeresis"
œ 	U+0153    C5_93         0153        "Latin Small Ligature Oe"
€ 	U+20AC    E2_82_AC      20AC        "Euro Sign"
東 	U+6771    E6_9D_B1      6771        "CJK Unified Ideograph-6771"
𝄞 	U+1D11E   F0_9D_84_9E   D834_DD1E   "Musical Symbol G Clef"
𠀇 	U+20007   F0_A0_80_87   D840_DC07   "CJK Unified Ideograph-20007"'''


def test_table() -> None:
    content = read("Table")
    text = ReliableTxt.decode(content)
    assert text == table


def test_empty() -> None:
    content = read("Empty")
    text = ReliableTxt.decode(content)
    assert text == ""


def test_four_lines() -> None:
    content = read("FourLines")
    text = ReliableTxt.decode(content)
    assert text == "Line 1\nLine 2\nLine 3\n"


def test_long_lines() -> None:
    content = read("LongLines")
    text = ReliableTxt.decode(content)
    supposed = "\n".join(
        "".join(f"LongLine{char}_{ix:03d}" for ix in range(1000)) for char in "AB"
    )
    assert text == supposed


def test_c0() -> None:
    content = read("C0")
    text = ReliableTxt.decode(content)
    assert text == "".join(chr(i) for i in range(32))


def test_unicode_line_breaks() -> None:
    content = read("UnicodeLineBreaks")
    text = ReliableTxt.decode(content)
    lines = text.split("\n")
    assert len(lines) == 3


def test_cjk() -> None:
    content = read("CJK")
    text = ReliableTxt.decode(content)
    # first 100 cjk characters
    assert text == "".join(chr(i) for i in range(0x4E00, 0x4E00 + 100))


def test_table_without_bom() -> None:
    content = read("TablewithoutBOM")
    with pytest.raises(ValueError):
        ReliableTxt.decode(content)


def test_corrupt_data() -> None:
    content = read("CorruptData")
    with pytest.raises(UnicodeDecodeError):
        ReliableTxt.decode(content)


test_empty()
test_four_lines()
test_long_lines()
test_table()
test_c0()
test_unicode_line_breaks()
test_cjk()
test_table_without_bom()
test_corrupt_data()
# %%
