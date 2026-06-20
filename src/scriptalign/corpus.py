"""Load parallel words from CSV into a domain-neutral :class:`ParallelCorpus`."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping

from .orthography import Orthography


@dataclass
class ParallelCorpus:
    """A pair of equal-length word lists plus their alphabets.

    ``words_a[i]`` and ``words_b[i]`` are aligned at the word level; the
    aligner discovers the within-word letter-level alignment.
    """

    words_a: list[str]
    words_b: list[str]
    alphabet_a: list[str]
    alphabet_b: list[str]
    script_a: Orthography
    script_b: Orthography

    def __post_init__(self) -> None:
        if len(self.words_a) != len(self.words_b):
            raise ValueError(
                f"Parallel corpora must have equal length "
                f"({len(self.words_a)} vs {len(self.words_b)})."
            )

    @property
    def n_words(self) -> int:
        return len(self.words_a)


def build_corpus(
    words_a: list[str],
    words_b: list[str],
    *,
    script_a: Orthography,
    script_b: Orthography,
) -> ParallelCorpus:
    """Wrap raw (pre-normalized) word lists into a corpus, applying each script's
    ``normalize`` + boundary characters and computing sorted alphabets."""
    wrapped_a = [script_a.wrap(w) for w in words_a]
    wrapped_b = [script_b.wrap(w) for w in words_b]
    alphabet_a = sorted(set("".join(wrapped_a)), key=script_a.sort_key)
    alphabet_b = sorted(set("".join(wrapped_b)), key=script_b.sort_key)
    return ParallelCorpus(
        words_a=wrapped_a,
        words_b=wrapped_b,
        alphabet_a=alphabet_a,
        alphabet_b=alphabet_b,
        script_a=script_a,
        script_b=script_b,
    )


def load_parallel_corpus(
    csv_path: str | Path,
    *,
    column_a: str,
    column_b: str,
    script_a: Orthography,
    script_b: Orthography,
    row_filter: Callable[[Mapping[str, str]], Mapping[str, str] | None] | None = None,
) -> ParallelCorpus:
    """Read parallel words from a CSV.

    ``row_filter``, if supplied, is called with each row as a ``dict`` and
    must return either a (possibly modified) mapping to keep, or ``None`` to
    drop the row. This is where domain-specific concerns live — column
    fallbacks, error flags, custom validation — keeping the library free of
    schema knowledge.
    """
    words_a: list[str] = []
    words_b: list[str] = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row_filter is not None:
                filtered = row_filter(dict(row))
                if filtered is None:
                    continue
                row = filtered
            words_a.append(row[column_a].strip())
            words_b.append(row[column_b].strip())
    return build_corpus(words_a, words_b, script_a=script_a, script_b=script_b)
