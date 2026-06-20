from pathlib import Path

import pytest

from scriptalign import Orthography, build_corpus, load_parallel_corpus

DATA = Path(__file__).parent / "data" / "tiny_parallel.csv"


def test_build_corpus_normalizes_and_sorts():
    a = Orthography(name="A", normalize=str.lower, sort_key=lambda c: -ord(c))
    b = Orthography(name="B")
    corpus = build_corpus(["AB", "BA"], ["xy", "yx"], script_a=a, script_b=b)
    assert corpus.words_a == ["ab", "ba"]
    assert corpus.alphabet_a == sorted({"a", "b"}, key=lambda c: -ord(c))
    assert corpus.alphabet_b == ["x", "y"]


def test_unequal_lengths_raise():
    a = b = Orthography(name="x")
    with pytest.raises(ValueError):
        build_corpus(["A"], ["x", "y"], script_a=a, script_b=b)


def test_load_with_row_filter():
    a = b = Orthography(name="x", boundary_start="^", boundary_end="$")

    def drop_bad(row):
        if row.get("skip"):
            return None
        return row

    corpus = load_parallel_corpus(
        DATA,
        column_a="side_a",
        column_b="side_b",
        script_a=a,
        script_b=b,
        row_filter=drop_bad,
    )
    # Six surviving rows (the one with skip="bad" is filtered out).
    assert corpus.n_words == 6
    assert all(w.startswith("^") and w.endswith("$") for w in corpus.words_a)
    assert all(w.startswith("^") and w.endswith("$") for w in corpus.words_b)
    assert set(corpus.alphabet_a) == {"^", "$", "A", "B"}
    assert set(corpus.alphabet_b) == {"^", "$", "x", "y"}


def test_row_filter_can_mutate():
    a = b = Orthography(name="x")

    def upper_a(row):
        return {**row, "side_a": row["side_a"].upper() + "!"}

    corpus = load_parallel_corpus(
        DATA,
        column_a="side_a",
        column_b="side_b",
        script_a=a,
        script_b=b,
        row_filter=upper_a,
    )
    assert all(w.endswith("!") for w in corpus.words_a)
