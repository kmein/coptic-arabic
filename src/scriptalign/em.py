"""EM-style refinement: alternate alignment and re-scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .align import align_pair
from .corpus import ParallelCorpus
from .scoring import (
    Counts,
    count_cooccurrences_aligned,
    count_cooccurrences_full,
    phi_from_counts,
)


@dataclass
class AlignmentResult:
    phi: np.ndarray
    counts: Counts
    alignments: list[list[tuple[int, int]]]
    corpus: ParallelCorpus


def iterate_alignment(
    corpus: ParallelCorpus,
    n_iters: int = 10,
    *,
    gap_scale: float = 0.5,
    on_iteration: Callable[[int, np.ndarray, list[list[tuple[int, int]]]], None] | None = None,
) -> AlignmentResult:
    """Bootstrap a φ matrix from Cartesian-product co-occurrences, then iterate:
    align every word pair against the current φ, recount co-occurrences from
    the alignments, recompute φ. After ``n_iters`` rounds return the final
    state.

    The optional ``on_iteration`` callback receives ``(iteration_index, phi,
    alignments)`` after each round and can be used to checkpoint intermediate
    matrices without coupling this module to disk I/O.
    """
    phi = phi_from_counts(count_cooccurrences_full(corpus))

    alignments: list[list[tuple[int, int]]] = []
    counts: Counts | None = None
    for iteration in range(n_iters):
        alignments = [
            align_pair(
                corpus.words_a[k],
                corpus.words_b[k],
                phi,
                corpus.alphabet_a,
                corpus.alphabet_b,
                gap_scale=gap_scale,
            )
            for k in range(corpus.n_words)
        ]
        counts = count_cooccurrences_aligned(corpus, alignments)
        phi = phi_from_counts(counts)
        if on_iteration is not None:
            on_iteration(iteration, phi, alignments)

    assert counts is not None  # n_iters >= 1
    return AlignmentResult(phi=phi, counts=counts, alignments=alignments, corpus=corpus)
