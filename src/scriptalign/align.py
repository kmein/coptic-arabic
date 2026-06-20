"""Pairwise sequence alignment via Needleman-Wunsch-style dynamic programming."""

from __future__ import annotations

from typing import Sequence

import numpy as np

# Backtrace arrow encoding (kept consistent with the legacy code):
#   0 = "left"     (consume one letter from sequence B; gap in A)
#   1 = "diagonal" (consume one letter from each)
#   2 = "up"       (consume one letter from sequence A; gap in B)
_LEFT, _DIAG, _UP = 0, 1, 2


def align_pair(
    word_a: str,
    word_b: str,
    score_matrix: np.ndarray,
    alphabet_a: Sequence[str],
    alphabet_b: Sequence[str],
    *,
    gap_scale: float = 0.5,
) -> list[tuple[int, int]]:
    """Align two words against a learned per-letter ``score_matrix``.

    Off-diagonal moves carry the predecessor cell's score scaled by
    ``gap_scale`` (instead of an additive gap penalty); on ties the diagonal
    move is preferred. Returns the alignment as a list of ``(i, j)`` pairs
    where ``i`` indexes ``word_a`` and ``j`` indexes ``word_b``.
    """
    index_a = {c: i for i, c in enumerate(alphabet_a)}
    index_b = {c: j for j, c in enumerate(alphabet_b)}

    n = len(word_a)
    m = len(word_b)

    scores = np.zeros((n, m))
    for i in range(n):
        ia = index_a[word_a[i]]
        for j in range(m):
            scores[i, j] = score_matrix[ia, index_b[word_b[j]]]

    align = np.zeros((n + 1, m + 1))
    arrow = np.zeros((n + 1, m + 1))
    arrow[:, 0] = _UP
    arrow[0, 0] = _DIAG

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            directions = [
                gap_scale * align[i, j - 1],
                align[i - 1, j - 1],
                gap_scale * align[i - 1, j],
            ]
            choice = int(np.argmax(directions))
            # Prefer diagonal on ties with either side.
            if (choice == _LEFT and directions[_LEFT] <= directions[_DIAG]) or (
                choice == _UP and directions[_UP] <= directions[_DIAG]
            ):
                choice = _DIAG
            align[i, j] = directions[choice] + scores[i - 1, j - 1]
            arrow[i, j] = choice

    i, j = n, m
    path: list[tuple[int, int]] = []
    while i > 0 and j > 0:
        path.insert(0, (i - 1, j - 1))
        step = arrow[i, j]
        if step > 0:
            i -= 1
        if step < 2:
            j -= 1
    return path
