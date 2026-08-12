#!/usr/bin/env python
"""Summarize a batch morphology results CSV.

Examples:
    python scripts/analyze_results.py
    python scripts/analyze_results.py --input outputs/simplified_particle_results.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

_SRC = Path(__file__).resolve().parents[1] / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agilentirformats.paths import FIXTURES_DIR, OUTPUTS_DIR  # noqa: E402


def summarize(df: pd.DataFrame) -> None:
    total_particles = len(df)
    small_particles = len(df[df["polymer"] == "small particle"])
    identified_particles = total_particles - small_particles

    print(f"Total particles found: {total_particles}")
    if total_particles:
        print(
            f"Small particles filtered: {small_particles} "
            f"({small_particles / total_particles * 100:.1f}%)"
        )
        print(
            f"Particles analyzed: {identified_particles} "
            f"({identified_particles / total_particles * 100:.1f}%)"
        )
    print()

    high_conf = len(df[df["best_pr"] >= 0.3])
    low_conf = len(df[(df["best_pr"] > 0) & (df["best_pr"] < 0.3)])
    no_conf = len(df[df["best_pr"] == 0.0])

    print("Confidence levels:")
    print(f"High confidence (≥0.3): {high_conf} particles")
    print(f"Low confidence (0-0.3): {low_conf} particles")
    print(f"No confidence (=0.0): {no_conf} particles")
    print()

    top_polymers = df[df["polymer"] != "small particle"].copy()
    if top_polymers.empty:
        print("No identified polymers to summarize.")
        return

    top_polymers["polymer_clean"] = top_polymers["polymer"].str.replace(
        r" \(low confidence\)", "", regex=True
    )
    polymer_counts = top_polymers["polymer_clean"].value_counts().head(10)

    print("Top 10 polymers identified:")
    for polymer, count in polymer_counts.items():
        high_conf_count = len(
            top_polymers[
                (top_polymers["polymer_clean"] == polymer)
                & (top_polymers["best_pr"] >= 0.3)
            ]
        )
        print(f"{polymer}: {count} total ({high_conf_count} high confidence)")

    print()
    print("Particle size distribution:")
    sizes = df[df["polymer"] != "small particle"]["pixel_count"]
    if len(sizes) > 0:
        print(f"Average particle size: {sizes.mean():.0f} pixels")
        print(f"Median particle size: {sizes.median():.0f} pixels")
        print(f"Largest particle: {sizes.max()} pixels")
        print(f"Smallest analyzed particle: {sizes.min()} pixels")
    else:
        print("No particle size data available")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize morphology analysis CSV results")
    parser.add_argument(
        "--input",
        "-i",
        help="Results CSV (default: outputs/simplified_particle_results.csv)",
    )
    args = parser.parse_args(argv)

    candidates = []
    if args.input:
        candidates.append(Path(args.input))
    else:
        candidates.extend(
            [
                OUTPUTS_DIR / "simplified_particle_results.csv",
                FIXTURES_DIR / "simplified_particle_results_with_area.csv",
            ]
        )

    csv_path = next((p for p in candidates if p.exists()), None)
    if csv_path is None:
        print("No results CSV found. Run batch analysis first, or pass --input.", file=sys.stderr)
        return 1

    print(f"Reading: {csv_path}")
    summarize(pd.read_csv(csv_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
