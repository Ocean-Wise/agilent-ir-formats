"""Repository path helpers.

Resolves locations relative to the repo root so scripts work no matter
which working directory they are launched from.
"""

from __future__ import annotations

from pathlib import Path

# src/agilentirformats/paths.py → repo root is parents[2]
REPO_ROOT = Path(__file__).resolve().parents[2]

INPUTS_DIR = REPO_ROOT / "inputs"
OUTPUTS_DIR = REPO_ROOT / "outputs"
LIBRARIES_DIR = REPO_ROOT / "data" / "libraries"
FIXTURES_DIR = REPO_ROOT / "data" / "fixtures"
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Polymer matching library (derivative-intensity cluster spectra)
DEFAULT_CLUSTER_LIBRARY = LIBRARIES_DIR / "OS_clusters_DERINT.csv"
DEFAULT_CLUSTER_INDEX = LIBRARIES_DIR / "OS_cluster_index.csv"
DEFAULT_FTIR_METADATA = LIBRARIES_DIR / "ftir_metadata_clusters.csv"
DEFAULT_OS_LIBRARY_DERINT = LIBRARIES_DIR / "open_specy_ftir_library_DERINT.csv"
DEFAULT_OS_LIBRARY_INT = LIBRARIES_DIR / "open_specy_ftir_library_INT.csv"


def ensure_work_dirs() -> None:
    """Create inputs/ and outputs/ if missing."""
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
