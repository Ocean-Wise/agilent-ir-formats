"""Tests for batch morphology helpers and CLI defaults."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from agilentirformats.cli_batch import find_dmt_files, main, match_library, parse_args
from agilentirformats.paths import DEFAULT_CLUSTER_LIBRARY, INPUTS_DIR, OUTPUTS_DIR


def test_find_dmt_files_recursive(tmp_path: Path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "sample.dmt").write_text("placeholder")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "b").mkdir()
    (tmp_path / "nested" / "b" / "other.dmt").write_text("placeholder")
    (tmp_path / "ignore.txt").write_text("nope")

    found = find_dmt_files(tmp_path)
    names = {p.name for p in found}
    assert names == {"sample.dmt", "other.dmt"}


def test_find_dmt_files_empty(tmp_path: Path):
    assert find_dmt_files(tmp_path) == []


def test_match_library_picks_best_row():
    library = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.5, 0.5, 0.0],
        ],
        dtype=np.float32,
    )
    spectrum = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    best_ix, best_pr = match_library(spectrum, library)
    assert best_ix == 1
    assert best_pr > 0.9


def test_match_library_all_nan_returns_sentinel():
    library = np.full((2, 3), np.nan, dtype=np.float32)
    spectrum = np.zeros(3, dtype=np.float32)
    best_ix, best_pr = match_library(spectrum, library)
    assert best_ix == -1
    assert best_pr == 0.0


def test_parse_args_defaults():
    args = parse_args([])
    assert args.input is None
    assert args.output is None
    assert Path(args.library) == DEFAULT_CLUSTER_LIBRARY
    assert args.min_pixels == 5
    assert args.non_interactive is False


def test_parse_args_custom_paths(tmp_path: Path):
    args = parse_args(
        [
            "--input",
            str(tmp_path / "in"),
            "--output",
            str(tmp_path / "out.csv"),
            "--min-pixels",
            "10",
            "--non-interactive",
        ]
    )
    assert args.input == str(tmp_path / "in")
    assert args.output == str(tmp_path / "out.csv")
    assert args.min_pixels == 10
    assert args.non_interactive is True


def test_main_noninteractive_missing_input_returns_error(tmp_path: Path):
    missing = tmp_path / "does-not-exist"
    code = main(["--input", str(missing), "--non-interactive"])
    assert code == 1


def test_main_noninteractive_empty_inputs_returns_error(tmp_path: Path):
    empty = tmp_path / "empty_inputs"
    empty.mkdir()
    out = tmp_path / "results.csv"
    code = main(
        [
            "--input",
            str(empty),
            "--output",
            str(out),
            "--non-interactive",
        ]
    )
    assert code == 1
    assert not out.exists()


def test_cli_defaults_point_at_repo_io_dirs():
    assert INPUTS_DIR.name == "inputs"
    assert OUTPUTS_DIR.name == "outputs"
    assert DEFAULT_CLUSTER_LIBRARY.name == "OS_clusters_DERINT.csv"
