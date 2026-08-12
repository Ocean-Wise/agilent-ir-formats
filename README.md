# agilent-ir-formats

Python tooling for **Agilent FTIR** hyperspectral files, used by Ocean Wise lab staff (admin: Stephanie Wang) to mass-review, edit, and analyse FTIR microplastic projects across many sample sessions.

Upstream reader: [Alex Henderson / University of Manchester](https://github.com/AlexHenderson/agilent-ir-formats) (MIT). This fork adds lab batch morphology analysis, polymer library matching, and a durable folder layout for session data.

## Start here

| Doc | When to use it |
|-----|----------------|
| [Lab workflow](docs/guides/lab-workflow.md) | Day-to-day: drop scans → run batch → review CSV |
| [Batch morphology](docs/guides/batch-morphology.md) | Inputs, outputs, CLI flags, algorithm notes |
| [Reading Agilent files](docs/guides/reading-agilent-files.md) | Using `AgilentIRFile` in Python |
| [Inputs & outputs](docs/reference/inputs-and-outputs.md) | What belongs in `inputs/` vs `outputs/` |
| [CSV contracts](docs/reference/csv-contracts.md) | Result and library column meanings |
| [Folder structure](docs/reference/folder-structure.md) | Where code, data, and docs live |
| [CONTRIBUTING](CONTRIBUTING.md) | PRs, branches, reviews — **do not commit straight to `main`** |
| [AGENTS](AGENTS.md) | Rules for AI agents working in this repo |

## Quick start (lab technicians)

1. **Install once** (Python ≥ 3.10):

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

2. **Drop session data** into `inputs/` (gitignored). Keep each Agilent project folder intact (`.dmt` plus companion files).

3. **Run batch analysis**:

   ```bash
   # Interactive (defaults to inputs/)
   python scripts/batch_morphology_analysis.py

   # Or non-interactive
   python scripts/batch_morphology_analysis.py --non-interactive

   # Windows: double-click scripts\run_analysis.bat
   ```

4. **Open results** under `outputs/` (gitignored), e.g. `outputs/simplified_particle_results.csv`.

5. **Summarize** (optional):

   ```bash
   python scripts/analyze_results.py
   ```

Polymer matching libraries live in `data/libraries/` (tracked). Sample result CSVs for docs/tests live in `data/fixtures/`.

Pull requests run lint + tests via [`.github/workflows/pr.yml`](.github/workflows/pr.yml). Locally: `ruff check src scripts tests && pytest -q`.

## Repo layout

```
agilent-ir-formats/
├── inputs/                 ← session .dmt projects (gitignored)
├── outputs/                ← analysis CSVs / plots (gitignored)
├── data/
│   ├── libraries/          ← Open Specy + cluster libraries (tracked)
│   └── fixtures/           ← small example CSVs (tracked)
├── src/agilentirformats/   ← installable Python package
├── scripts/                ← lab CLIs + Windows launcher
│   └── legacy/             ← one-off patch / timing scripts
├── notebooks/              ← exploratory analysis
├── docs/                   ← guides + reference
└── tests/
```

## Safety — what never gets committed

- Raw Agilent scans and project folders (`inputs/`)
- Analysis dumps, plots, and session CSVs (`outputs/`)
- Virtualenvs (`.venv/`, `.conda/`), secrets (`.env`)

Reference libraries under `data/libraries/` **are** committed so the matching pipeline works out of the box.

## Upstream file reader

```python
from pprint import pprint
from agilentirformats import AgilentIRFile

reader = AgilentIRFile()
reader.read(r"inputs/my_project/myfile.dmt")

print(reader.xvalues.shape)
print(reader.intensities.shape)
pprint(reader.metadata)
```

Requirements for the reader alone: `python >= 3.10`, `h5py`, `numpy`. Full lab tooling also needs `pandas`, `scikit-learn`, `scikit-image`, `scipy` (installed via `pip install -e .`).

## Licence

Copyright (c) 2018–2023 Alex Henderson — MIT. See [LICENSE](LICENSE).  
Ocean Wise lab scripts and documentation in this repository follow the same MIT licence unless noted otherwise.

Upstream: https://github.com/AlexHenderson/agilent-ir-formats  
MATLAB sibling: https://bitbucket.org/AlexHenderson/agilent-file-formats/
