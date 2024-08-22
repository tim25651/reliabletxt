import pytest
from whitespacesv import chars_to_ords, ords_to_chars


def test_ords_to_chars():
    ords = [97, 98, 99]
    expected_result = "abc"
    assert ords_to_chars(ords) == expected_result


def test_ords_to_chars_empty():
    ords = []
    expected_result = ""
    assert ords_to_chars(ords) == expected_result


def test_chars_to_ords():
    chars = "abc"
    expected_result = [97, 98, 99]
    assert chars_to_ords(chars) == expected_result


def test_chars_to_ords_empty():
    chars = ""
    expected_result = []
    assert chars_to_ords(chars) == expected_result
