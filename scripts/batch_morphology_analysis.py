#!/usr/bin/env python
"""CLI wrapper — prefer installing the package, then ``agilent-batch-morphology``.

This script remains for double-click / bat launchers and local development:

    python scripts/batch_morphology_analysis.py
    python scripts/batch_morphology_analysis.py --input inputs/my_session --non-interactive
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running without an editable install by putting src/ on sys.path
_SRC = Path(__file__).resolve().parents[1] / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agilentirformats.cli_batch import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
