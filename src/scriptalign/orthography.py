"""Describe a writing system: how to normalize words and how to order letters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


def _identity(s: str) -> str:
    return s


def _identity_key(c: str) -> Any:
    return c


@dataclass(frozen=True)
class Orthography:
    """A writing system's per-word normalizer, per-letter sort key, and optional boundary anchors.

    Boundary characters, when supplied, are prepended and appended to every
    word during corpus loading. They give the aligner stable end-of-word anchor
    points and are treated as members of the alphabet.
    """

    name: str
    normalize: Callable[[str], str] = field(default=_identity)
    sort_key: Callable[[str], Any] = field(default=_identity_key)
    boundary_start: str | None = None
    boundary_end: str | None = None

    def wrap(self, word: str) -> str:
        out = self.normalize(word)
        if self.boundary_start is not None:
            out = self.boundary_start + out
        if self.boundary_end is not None:
            out = out + self.boundary_end
        return out
