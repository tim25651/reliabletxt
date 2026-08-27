"""The main module of the reliabletxt package."""

from __future__ import annotations

from reliabletxt._reliabletxt import ReliableTxtCharIterator, ReliableTxtDocument, decode, encode

__all__ = ["ReliableTxtCharIterator", "ReliableTxtDocument", "decode", "encode"]
