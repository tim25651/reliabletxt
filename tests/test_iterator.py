"""Tests for the ReliableTxtCharIterator class."""

from __future__ import annotations

from reliabletxt import ReliableTxtCharIterator


def test_iterator_starts_at_zero() -> None:
    iterator = ReliableTxtCharIterator("ab")
    assert iterator.ix == 0
    assert not iterator.is_eof()


def test_iterator_forward_reaches_eof() -> None:
    iterator = ReliableTxtCharIterator("a")
    iterator.forward()
    assert iterator.ix == 1
    assert iterator.is_eof()


def test_iterator_is_eof_on_empty_text() -> None:
    assert ReliableTxtCharIterator("").is_eof()


def test_is_char_false_at_eof() -> None:
    assert not ReliableTxtCharIterator("").is_char("a")


def test_try_read_char_advances_on_match() -> None:
    iterator = ReliableTxtCharIterator("ab")
    assert iterator.try_read_char("a")
    assert iterator.ix == 1


def test_try_read_char_does_not_advance_on_mismatch() -> None:
    iterator = ReliableTxtCharIterator("ab")
    assert not iterator.try_read_char("b")
    assert iterator.ix == 0


def test_get_line_info_tracks_line_and_column() -> None:
    iterator = ReliableTxtCharIterator("ab\ncd")
    for _ in range(4):
        iterator.forward()
    assert iterator.get_line_info() == (1, 1)
