"""
Unit tests for the `filter_pre_commit_hooks` module.
"""

import pytest

from filter_pre_commit_hooks.filter_pre_commit_hooks import (
    Format,
    Hook,
    Mode,
    Orient,
    Target,
    extract_tags,
    format_hooks,
    is_hook_filtered,
)


@pytest.mark.parametrize(
    ("alias", "expected"),
    [
        pytest.param(
            id="no_alias",
            *[None, set()],
        ),
        pytest.param(
            id="empty_alias",
            *["", set()],
        ),
        pytest.param(
            id="happy",
            *["x (a, b)", {"a", "b"}],
        ),
        pytest.param(
            id="no_space",
            *["x (a,b)", {"a", "b"}],
        ),
        pytest.param(
            id="duplicate",
            *["x (a, b, b)", {"a", "b"}],
        ),
    ],
)
def test_extract_tags(alias: str | None, expected: set[str]) -> None:
    """Test the `extract_tags` function."""

    assert extract_tags(alias) == expected


@pytest.mark.parametrize(
    ("hook", "filters", "target", "mode", "orient", "expected"),
    [
        pytest.param(
            id="basic",
            *[
                {"alias": "x (a, b)"},
                ["a", "b"],
                Target.TAG,
                Mode.ALL_OF,
                Orient.NO_INVERT,
                True,
            ],
        ),
        pytest.param(
            id="inverted_mode",
            *[
                {"alias": "x (a, b)"},
                ["a", "b"],
                Target.TAG,
                Mode.ALL_OF,
                Orient.INVERT,
                False,
            ],
        ),
        pytest.param(
            id="not_all_tags_present",
            *[
                {"alias": "x (a, b)"},
                ["a", "b", "c"],
                Target.TAG,
                Mode.ALL_OF,
                Orient.NO_INVERT,
                False,
            ],
        ),
        pytest.param(
            id="any_tag_is_fine",
            *[
                {"alias": "x (a)"},
                ["a", "b"],
                Target.TAG,
                Mode.ANY_OF,
                Orient.NO_INVERT,
                True,
            ],
        ),
        pytest.param(
            id="alias_missing",
            *[
                {},
                ["a", "b"],
                Target.TAG,
                Mode.ALL_OF,
                Orient.NO_INVERT,
                False,
            ],
        ),
        pytest.param(
            id="any_id_is_fine",
            *[
                {"id": "x"},
                ["x", "y"],
                Target.ID,
                Mode.ANY_OF,
                Orient.NO_INVERT,
                True,
            ],
        ),
        pytest.param(
            id="all_ids_must_be_given",
            *[
                {"id": "x"},
                ["x", "y"],
                Target.ID,
                Mode.ALL_OF,
                Orient.NO_INVERT,
                False,
            ],
        ),
        pytest.param(
            id="all_of_same_id",
            *[
                {"id": "x"},
                ["x", "x"],
                Target.ID,
                Mode.ALL_OF,
                Orient.NO_INVERT,
                True,
            ],
        ),
    ],
)
def test_hook_is_filtered(  # noqa: PLR0913
    hook: Hook,
    filters: list[str],
    target: Target,
    mode: Mode,
    orient: Orient,
    expected: bool,  # noqa: FBT001
) -> None:
    """Test the `is_hook_filtered` method."""

    assert is_hook_filtered(hook, filters, target, mode, orient) is expected


@pytest.mark.parametrize(
    ("hooks", "output_format", "expected"),
    [
        pytest.param(
            id="comma_separated",
            *[
                {"hook1", "hook2", "hook3"},
                Format.COMMA,
                "hook1, hook2, hook3",
            ],
        ),
        pytest.param(
            id="newline_separated",
            *[
                {"hook1", "hook2", "hook3"},
                Format.NEWLINE,
                "hook1\nhook2\nhook3",
            ],
        ),
        pytest.param(
            id="empty_set",
            *[
                set(),
                Format.COMMA,
                "",
            ],
        ),
        pytest.param(
            id="single_hook",
            *[
                {"hook1"},
                Format.COMMA,
                "hook1",
            ],
        ),
    ],
)
def test_format_hooks(
    hooks: set[str],
    output_format: Format,
    expected: str,
) -> None:
    """Test the `format_hooks` function."""

    assert format_hooks(hooks, output_format) == expected
