"""Co-occurrence counts and φ-coefficient scoring matrix."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .corpus import ParallelCorpus


@dataclass
class Counts:
    """Co-occurrence statistics for two parallel alphabets.

    ``occurrences[i, j]`` is the number of times letter ``alphabet_a[i]`` was
    observed in a pair with letter ``alphabet_b[j]``. ``totals_a`` and
    ``totals_b`` are the marginals; ``total`` is the grand total of pairs.
    """

    occurrences: np.ndarray
    totals_a: np.ndarray
    totals_b: np.ndarray
    total: int


def count_cooccurrences_full(corpus: ParallelCorpus) -> Counts:
    """Seed counts using every (letter_a, letter_b) pair across each word's
    Cartesian product — the unaligned baseline used to bootstrap the iteration."""
    alphabet_a = corpus.alphabet_a
    alphabet_b = corpus.alphabet_b
    index_a = {c: i for i, c in enumerate(alphabet_a)}
    index_b = {c: j for j, c in enumerate(alphabet_b)}

    occurrences = np.zeros((len(alphabet_a), len(alphabet_b)))
    totals_a = np.zeros((len(alphabet_a), 1))
    totals_b = np.zeros((1, len(alphabet_b)))
    total = 0

    for word_a, word_b in zip(corpus.words_a, corpus.words_b):
        for ca in word_a:
            i = index_a[ca]
            for cb in word_b:
                j = index_b[cb]
                occurrences[i, j] += 1
                totals_a[i, 0] += 1
                totals_b[0, j] += 1
                total += 1

    return Counts(occurrences, totals_a, totals_b, total)


def count_cooccurrences_aligned(
    corpus: ParallelCorpus,
    alignments: Sequence[Sequence[tuple[int, int]]],
) -> Counts:
    """Count only the (i, j) letter pairs produced by the aligner."""
    alphabet_a = corpus.alphabet_a
    alphabet_b = corpus.alphabet_b
    index_a = {c: i for i, c in enumerate(alphabet_a)}
    index_b = {c: j for j, c in enumerate(alphabet_b)}

    occurrences = np.zeros((len(alphabet_a), len(alphabet_b)))
    totals_a = np.zeros((len(alphabet_a), 1))
    totals_b = np.zeros((1, len(alphabet_b)))
    total = 0

    for word_a, word_b, alignment in zip(corpus.words_a, corpus.words_b, alignments):
        for ia, ib in alignment:
            i = index_a[word_a[ia]]
            j = index_b[word_b[ib]]
            occurrences[i, j] += 1
            totals_a[i, 0] += 1
            totals_b[0, j] += 1
            total += 1

    return Counts(occurrences, totals_a, totals_b, total)


def phi_from_counts(counts: Counts) -> np.ndarray:
    """φ coefficient for every letter pair, normalized so the largest absolute
    value is 1. Zero denominators are clamped to 0.01 (preserves legacy
    behavior from the original Casey implementation)."""
    n_a, n_b = counts.occurrences.shape
    phi = np.zeros((n_a, n_b))
    for i in range(n_a):
        for j in range(n_b):
            a = counts.occurrences[i, j]
            b = counts.totals_b[0, j] - a
            c = counts.totals_a[i, 0] - a
            d = counts.total - b - c + a
            denom = ((a + b) * (c + d) * (a + c) * (b + d)) ** 0.5
            denom = denom if denom else 0.01
            phi[i, j] = (a * d - b * c) / denom
    peak = np.max(np.abs(phi))
    if peak:
        phi /= peak
    return phi
