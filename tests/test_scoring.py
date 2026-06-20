import numpy as np

from scriptalign import (
    Counts,
    Orthography,
    build_corpus,
    count_cooccurrences_aligned,
    count_cooccurrences_full,
    phi_from_counts,
)


def _corpus(words_a, words_b):
    a = b = Orthography(name="x")
    return build_corpus(words_a, words_b, script_a=a, script_b=b)


def test_full_counts_match_cartesian_product():
    corpus = _corpus(["AB"], ["xy"])  # one word, 2x2 product
    counts = count_cooccurrences_full(corpus)
    assert counts.total == 4
    assert int(counts.totals_a[corpus.alphabet_a.index("A"), 0]) == 2
    assert int(counts.totals_b[0, corpus.alphabet_b.index("y")]) == 2
    assert int(counts.occurrences[corpus.alphabet_a.index("A"),
                                  corpus.alphabet_b.index("x")]) == 1


def test_aligned_counts_only_count_aligned_pairs():
    corpus = _corpus(["AB"], ["xy"])
    counts = count_cooccurrences_aligned(corpus, [[(0, 0), (1, 1)]])
    assert counts.total == 2
    assert int(counts.occurrences[corpus.alphabet_a.index("A"),
                                  corpus.alphabet_b.index("x")]) == 1
    assert int(counts.occurrences[corpus.alphabet_a.index("B"),
                                  corpus.alphabet_b.index("y")]) == 1


def test_phi_perfectly_correlated_yields_unit():
    """Two letters that always co-occur should produce phi = +1 normalized."""
    occ = np.array([[5.0, 0.0], [0.0, 5.0]])
    ta = np.array([[5.0], [5.0]])
    tb = np.array([[5.0, 5.0]])
    counts = Counts(occurrences=occ, totals_a=ta, totals_b=tb, total=10)
    phi = phi_from_counts(counts)
    # Diagonal entries are perfectly correlated; both become +1 after the
    # max-abs normalization.
    assert phi[0, 0] == 1.0
    assert phi[1, 1] == 1.0
    # Off-diagonal: perfect anti-correlation -> -1.
    assert phi[0, 1] == -1.0
    assert phi[1, 0] == -1.0


def test_phi_zero_denominator_does_not_crash():
    # A column with zero marginal: every entry in that column has b+d=0,
    # which (without the guard) would 0/0.
    occ = np.zeros((2, 2))
    occ[0, 0] = 3
    occ[1, 0] = 2
    ta = np.array([[3.0], [2.0]])
    tb = np.array([[5.0, 0.0]])
    counts = Counts(occurrences=occ, totals_a=ta, totals_b=tb, total=5)
    phi = phi_from_counts(counts)  # must not raise
    assert phi.shape == (2, 2)
    assert np.all(np.isfinite(phi))
