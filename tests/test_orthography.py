from scriptalign import Orthography


def test_identity_defaults():
    o = Orthography(name="x")
    assert o.wrap("hello") == "hello"
    assert o.sort_key("a") == "a"


def test_boundaries_applied():
    o = Orthography(name="x", boundary_start="<", boundary_end=">")
    assert o.wrap("ab") == "<ab>"


def test_normalize_runs_before_boundaries():
    def upper(s):
        return s.upper()

    o = Orthography(name="x", normalize=upper, boundary_start="^", boundary_end="$")
    assert o.wrap("ab") == "^AB$"


def test_custom_sort_key():
    o = Orthography(name="x", sort_key=lambda c: (-ord(c), c))
    letters = sorted(["a", "z", "m"], key=o.sort_key)
    assert letters == ["z", "m", "a"]


def test_only_one_boundary():
    o = Orthography(name="x", boundary_start="<")
    assert o.wrap("ab") == "<ab"
    o = Orthography(name="x", boundary_end=">")
    assert o.wrap("ab") == "ab>"
