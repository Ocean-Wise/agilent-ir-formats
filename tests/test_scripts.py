"""Entrypoint / packaging smoke tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "script",
    [
        "scripts/batch_morphology_analysis.py",
        "scripts/analyze_results.py",
    ],
)
def test_script_help_exits_zero(script: str):
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / script), "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout.lower() or "usage:" in result.stderr.lower()


def test_console_script_help():
    result = subprocess.run(
        [sys.executable, "-m", "agilentirformats.cli_batch", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_fixture_csv_has_expected_columns():
    import pandas as pd

    from agilentirformats.paths import FIXTURES_DIR

    path = FIXTURES_DIR / "simplified_particle_results_with_area.csv"
    df = pd.read_csv(path)
    for col in ("polymer", "best_pr", "pixel_count"):
        assert col in df.columns
