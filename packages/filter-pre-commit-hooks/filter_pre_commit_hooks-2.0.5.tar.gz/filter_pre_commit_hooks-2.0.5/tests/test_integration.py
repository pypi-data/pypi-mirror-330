"""
Integration tests for the `filter_pre_commit_hooks` module.
"""

from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from filter_pre_commit_hooks.filter_pre_commit_hooks import (
    Command,
    filter_pre_commit_hooks,
)


def test_cli_help() -> None:
    """Test the CLI help message."""

    result = CliRunner().invoke(filter_pre_commit_hooks, ["--help"])

    assert result.exit_code == 0


def test_command() -> None:
    """
    Test that the custom command handles missing epilog.
    """

    @click.command(
        cls=Command,
    )
    def command() -> None:
        pass

    CliRunner().invoke(command, ["--help"])


def test_invalid_config(tmp_path: Path) -> None:
    """
    Test that program fails with error message when invalid config is provided.
    """

    invalid_config = tmp_path / "invalid.yaml"
    invalid_config.write_text("invalid")

    result = CliRunner().invoke(
        filter_pre_commit_hooks,
        ["--config", str(invalid_config.absolute())],
    )

    assert result.output == "Failed to parse config.\n"
    assert result.exit_code == 1


@pytest.mark.parametrize(
    ("extra_args", "expected"),
    [
        pytest.param(
            id="default",
            *[
                ["check", "task"],
                ", ".join(  # noqa: FLY002
                    [
                        "end-of-file-fixer",
                        "fix-byte-order-marker",
                        "shellcheck",
                        "shfmt",
                        "yamlfmt",
                    ]
                )
                + "\n",
            ],
        ),
        pytest.param(
            id="no_invert",
            *[
                ["--orient=no-invert", "check", "task"],
                ", ".join(  # noqa: FLY002
                    [
                        "check-added-large-files",
                        "check-merge-conflict",
                    ]
                )
                + "\n",
            ],
        ),
        pytest.param(
            id="id_all_of",
            *[
                ["--target=id", "check-added-large-files", "shfmt", "shfmt"],
                ", ".join(  # noqa: FLY002
                    [
                        "check-added-large-files",
                        "check-merge-conflict",
                        "end-of-file-fixer",
                        "fix-byte-order-marker",
                        "shellcheck",
                        "shfmt",
                        "yamlfmt",
                    ]
                )
                + "\n",
            ],
        ),
        pytest.param(
            id="id_realistic",
            *[
                ["--target=id", "--mode=any-of", "shfmt", "shellcheck", "yamlfmt"],
                ", ".join(  # noqa: FLY002
                    [
                        "check-added-large-files",
                        "check-merge-conflict",
                        "end-of-file-fixer",
                        "fix-byte-order-marker",
                    ]
                )
                + "\n",
            ],
        ),
    ],
)
def test_cli(extra_args: list[str], expected: str) -> None:
    """Test the CLI."""

    result = CliRunner().invoke(
        filter_pre_commit_hooks,
        ["--config", "tests/resources/pre-commit-config.yaml", *extra_args],
    )

    assert result.output == expected
    assert result.exit_code == 0
