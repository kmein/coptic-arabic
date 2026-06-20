"""Human-readable views of alignments and scoring matrices."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def format_word_alignment(
    word_a: str,
    word_b: str,
    alignment: Sequence[tuple[int, int]],
) -> str:
    """Render a single word's alignment as a four-row tab-separated block:
    indices in B, letters in B, letters in A, indices in A.

    Matches the layout produced by the legacy ``improve_alignment.py``.
    """
    idx_a = [str(p[0]) for p in alignment]
    idx_b = [str(p[1]) for p in alignment]
    chars_a = [word_a[p[0]] for p in alignment]
    chars_b = [word_b[p[1]] for p in alignment]
    rows = ["\t".join(chars_b), "\t".join(idx_b), "\t".join(idx_a), "\t".join(chars_a)]
    return "\n".join(rows)


def format_phi_table(
    phi: np.ndarray,
    alphabet_a: Sequence[str],
    alphabet_b: Sequence[str],
    *,
    scale: float = 1.0,
) -> str:
    """Render φ as a tab-separated table with column headers (alphabet_b) and
    row headers (alphabet_a). Useful for pasting into a spreadsheet."""
    header = "\t" + "\t".join(alphabet_b)
    rows = [
        alphabet_a[i] + "\t" + "\t".join(f"{phi[i, j] * scale:f}" for j in range(phi.shape[1]))
        for i in range(phi.shape[0])
    ]
    return header + "\n" + "\n".join(rows)
