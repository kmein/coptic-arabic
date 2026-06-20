"""Discover letter-level correspondences between two parallel orthographies."""

from .align import align_pair
from .corpus import ParallelCorpus, build_corpus, load_parallel_corpus
from .em import AlignmentResult, iterate_alignment
from .formatting import format_phi_table, format_word_alignment
from .io_ import load_legacy_state, load_state, save_matrix_csv, save_state
from .orthography import Orthography
from .scoring import (
    Counts,
    count_cooccurrences_aligned,
    count_cooccurrences_full,
    phi_from_counts,
)

__all__ = [
    "AlignmentResult",
    "Counts",
    "Orthography",
    "ParallelCorpus",
    "align_pair",
    "build_corpus",
    "count_cooccurrences_aligned",
    "count_cooccurrences_full",
    "format_phi_table",
    "format_word_alignment",
    "iterate_alignment",
    "load_legacy_state",
    "load_parallel_corpus",
    "load_state",
    "phi_from_counts",
    "save_matrix_csv",
    "save_state",
]
