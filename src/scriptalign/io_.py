"""Disk I/O helpers — separate from the pure algorithmic core."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import numpy as np

from .corpus import ParallelCorpus


def save_matrix_csv(path: str | Path, matrix: np.ndarray) -> None:
    np.savetxt(path, matrix, delimiter=",")


def save_state(
    path: str | Path,
    corpus: ParallelCorpus,
    alignments: list[list[tuple[int, int]]],
) -> None:
    """Persist the current corpus + alignments to a pickle.

    The schema is dict-keyed (``words_a``, ``words_b``, ``alignments``) and
    domain-neutral. See :func:`load_legacy_state` for reading the original
    Coptic-Arabic ``aligned_texts.p`` shape.
    """
    payload = {
        "words_a": corpus.words_a,
        "words_b": corpus.words_b,
        "alignments": [list(a) for a in alignments],
    }
    with open(path, "wb") as f:
        pickle.dump(payload, f)


def load_state(path: str | Path) -> dict[str, Any]:
    with open(path, "rb") as f:
        return pickle.load(f)


def load_legacy_state(path: str | Path) -> dict[str, Any]:
    """Read the historic ``aligned_texts.p`` whose keys were ``Coptic`` /
    ``Arabic`` / ``Alignments``. Returns a dict in the new schema."""
    with open(path, "rb") as f:
        legacy = pickle.load(f)
    return {
        "words_a": legacy["Coptic"],
        "words_b": legacy["Arabic"],
        "alignments": legacy["Alignments"],
    }
