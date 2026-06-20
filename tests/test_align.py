import numpy as np

from scriptalign import align_pair


def test_identity_alignment_is_diagonal():
    alphabet = ["A", "B"]
    # Identity score matrix: perfect correlation on the diagonal.
    score = np.eye(2)
    path = align_pair("AB", "AB", score, alphabet, alphabet)
    assert path == [(0, 0), (1, 1)]


def test_insertion_in_b():
    alphabet = ["A", "B", "C"]
    score = np.eye(3) - 0.5 * (1 - np.eye(3))  # diagonal = 1, off = -0.5
    # Word B has an extra letter that doesn't appear in A.
    path = align_pair("AC", "ABC", score, alphabet, alphabet)
    # The two real correspondences (A-A and C-C) should both be present.
    pairs = set(path)
    assert (0, 0) in pairs  # A-A
    assert (1, 2) in pairs  # C-C


def test_tie_prefers_diagonal():
    """When the left and diagonal predecessors are equal, the legacy
    implementation prefers the diagonal move. Verify the port retains that."""
    alphabet = ["A", "B"]
    score = np.zeros((2, 2))  # all zeros -> every direction tied
    path = align_pair("AB", "AB", score, alphabet, alphabet)
    assert path == [(0, 0), (1, 1)]
