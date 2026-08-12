"""Tests for results summarizer CLI."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from agilentirformats.paths import FIXTURES_DIR


def test_analyze_results_main_uses_fixture(capsys):
    import importlib.util

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "analyze_results.py"
    spec = importlib.util.spec_from_file_location("analyze_results_script", script_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    fixture = FIXTURES_DIR / "simplified_particle_results_with_area.csv"
    assert fixture.is_file()

    code = mod.main(["--input", str(fixture)])
    assert code == 0
    captured = capsys.readouterr().out
    assert "Total particles found:" in captured
    assert "Top 10 polymers" in captured or "No identified polymers" in captured


def test_summarize_handles_empty_identified(capsys):
    import importlib.util

    script_path = Path(__file__).resolve().parents[1] / "scripts" / "analyze_results.py"
    spec = importlib.util.spec_from_file_location("analyze_results_script", script_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    df = pd.DataFrame(
        {
            "polymer": ["small particle", "small particle"],
            "best_pr": [0.0, 0.0],
            "pixel_count": [1, 2],
        }
    )
    mod.summarize(df)
    out = capsys.readouterr().out
    assert "Total particles found: 2" in out
    assert "No identified polymers" in out
