"""Command-line entry point: reproduce the original Casey alignment outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from scriptalign import (
    AlignmentResult,
    format_phi_table,
    iterate_alignment,
    save_correspondences_tsv,
    save_labeled_matrix_csv,
    save_matrix_csv,
    save_state,
)

from .corpus_config import load_corpus


def _write_outputs(result: AlignmentResult, output_dir: Path, iteration: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    a, b = result.corpus.alphabet_a, result.corpus.alphabet_b
    save_matrix_csv(
        output_dir / f"Co-occurrences (after alignment #{iteration}).csv",
        result.counts.occurrences,
    )
    save_matrix_csv(
        output_dir / f"phi (after alignment #{iteration}).csv",
        result.phi,
    )
    save_labeled_matrix_csv(output_dir / "correspondences.csv", result.phi, a, b)
    save_correspondences_tsv(
        output_dir / "correspondences_ranked.tsv", result.phi, a, b
    )
    save_state(output_dir / "aligned_texts.pkl", result.corpus, result.alignments)


def run(
    input_path: Path,
    output_dir: Path,
    *,
    iterations: int = 10,
    gap_scale: float = 0.5,
    clipboard: bool = False,
) -> AlignmentResult:
    corpus = load_corpus(input_path)
    result = iterate_alignment(corpus, n_iters=iterations, gap_scale=gap_scale)
    _write_outputs(result, output_dir, iteration=iterations - 1)

    if clipboard:
        import pyperclip  # lazy: only require it on this code path

        pyperclip.copy(
            format_phi_table(result.phi, corpus.alphabet_a, corpus.alphabet_b, scale=10.0)
        )

    return result


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="coptic-arabic",
        description="Run the Coptic-Arabic letter-alignment pipeline.",
    )
    parser.add_argument("--input", type=Path, default=Path("parallel_texts.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--gap-scale", type=float, default=0.5)
    parser.add_argument(
        "--clipboard",
        action="store_true",
        help="Copy the final phi table to the clipboard (requires pyperclip).",
    )
    args = parser.parse_args(argv)
    run(
        input_path=args.input,
        output_dir=args.output_dir,
        iterations=args.iterations,
        gap_scale=args.gap_scale,
        clipboard=args.clipboard,
    )


if __name__ == "__main__":
    main()
