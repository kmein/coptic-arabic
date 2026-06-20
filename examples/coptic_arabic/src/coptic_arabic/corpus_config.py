"""How this particular CSV maps onto :class:`scriptalign.ParallelCorpus`."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from scriptalign import ParallelCorpus, load_parallel_corpus

from .orthographies import ARABIC, COPTIC

COPTIC_COLUMN = "Coptic-Arabic"
ARABIC_COLUMN = "Arabic"
VOCALIZED_COLUMN = "Vocalized"
ERROR_COLUMN = "Error"


def _row_filter(row: Mapping[str, str]) -> dict[str, str] | None:
    """Drop rows flagged with an error; otherwise prefer the vocalized Arabic
    form over the plain one and drop rows missing it."""
    if row.get(ERROR_COLUMN):
        return None
    vocalized = row.get(VOCALIZED_COLUMN, "").strip()
    if not vocalized:
        return None
    return {**dict(row), ARABIC_COLUMN: vocalized}


def load_corpus(csv_path: str | Path) -> ParallelCorpus:
    return load_parallel_corpus(
        csv_path,
        column_a=COPTIC_COLUMN,
        column_b=ARABIC_COLUMN,
        script_a=COPTIC,
        script_b=ARABIC,
        row_filter=_row_filter,
    )
