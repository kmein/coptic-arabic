"""Coptic-Arabic letter alignment — an example client of the scriptalign library.

This package supplies the corpus-specific knobs (Coptic and Arabic
:class:`Orthography` definitions, CSV column names, row filtering) that
:mod:`scriptalign` deliberately does not bake in.
"""

from .orthographies import ARABIC, COPTIC
from .corpus_config import load_corpus

__all__ = ["ARABIC", "COPTIC", "load_corpus"]
