# Folder structure

```
agilent-ir-formats/
├── AGENTS.md                 # Rules for AI agents
├── CONTRIBUTING.md           # PR workflow (no direct commits to main)
├── README.md                 # Lab + developer entry point
├── pyproject.toml            # Package metadata + dependencies
├── CITATION.cff
├── LICENSE
│
├── inputs/                   # Session Agilent projects (gitignored)
├── outputs/                  # Analysis products (gitignored)
│
├── data/
│   ├── libraries/            # Open Specy + cluster CSVs (tracked)
│   └── fixtures/             # Small example results (tracked)
│
├── src/agilentirformats/     # Installable package
│   ├── agilent_ir_file.py    # Upstream Agilent reader
│   ├── paths.py              # Repo-root path constants
│   ├── cli_batch.py          # Batch morphology CLI implementation
│   ├── library_OS_fit.py     # Polymer ID helpers
│   ├── agilent_to_python.py
│   ├── calc_pca.py
│   └── spec_process.py
│
├── scripts/                  # Thin CLIs / Windows bat
│   ├── batch_morphology_analysis.py
│   ├── analyze_results.py
│   ├── run_analysis.bat
│   └── legacy/               # One-off historical scripts
│
├── notebooks/                # Exploratory notebooks
├── docs/
│   ├── guides/
│   ├── reference/
│   └── changes/
└── tests/
```

## Rules of thumb

- **New analysis code** → `src/agilentirformats/`
- **New lab command** → `scripts/` + docs under `docs/guides/`
- **Session scans** → `inputs/` only
- **Generated CSVs/plots** → `outputs/` only
- **Shared reference spectra** → `data/libraries/`
- **Do not** add new loose files at the repository root without updating this doc and `AGENTS.md`
