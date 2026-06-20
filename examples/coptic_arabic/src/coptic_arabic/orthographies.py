"""Coptic and Arabic orthography definitions used by this corpus."""

from __future__ import annotations

import re

from scriptalign import Orthography

_ARABIC_TERMINAL_DIACRITICS = frozenset(chr(c) for c in range(0x064B, 0x0660))
_ARABIC_SUKUN = "ْ"
_COPTIC_RARE_LETTERS_PATTERN = re.compile(r"([ϣ-ϯϢ-Ϯ])")
_BOUNDARY_START = "ª"
_BOUNDARY_END = "º"


def _strip_coptic_ticks(word: str) -> str:
    return word.replace("'", "")


def _coptic_sort_key(letter: str) -> str:
    # The rare letters ϣ-ϯ sort after ⲱ (omega); ȣ is treated as the digraph ⲩ + ȣ
    # so it sorts immediately after ⲩ instead of where the codepoint would put it.
    return _COPTIC_RARE_LETTERS_PATTERN.sub(r"ⲱ\1", letter.replace("ȣ", "ⲩȣ"))


def _strip_arabic_diacritics(word: str) -> str:
    word = word.replace(_ARABIC_SUKUN, "")
    if word and word[-1] in _ARABIC_TERMINAL_DIACRITICS:
        word = word[:-1]
    return word


COPTIC = Orthography(
    name="Coptic",
    normalize=_strip_coptic_ticks,
    sort_key=_coptic_sort_key,
    boundary_start=_BOUNDARY_START,
    boundary_end=_BOUNDARY_END,
)

ARABIC = Orthography(
    name="Arabic",
    normalize=_strip_arabic_diacritics,
    boundary_start=_BOUNDARY_START,
    boundary_end=_BOUNDARY_END,
)
