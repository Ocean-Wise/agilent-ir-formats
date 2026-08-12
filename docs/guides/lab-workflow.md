# Lab workflow — FTIR batch review

For lab technicians running Agilent FTIR microplastic sessions (administrator: Stephanie Wang).

## One-time setup

1. Install [Python 3.10+](https://www.python.org/downloads/).
2. In this repository:

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. On Windows you can also use `scripts\run_analysis.bat` after the venv exists (or with a conda env that provides `python`).

## Every sample session

### 1. Import data

Copy each Agilent **project folder** (the `.dmt` file and its companion files) into `inputs/`.

```
inputs/
  sample_A_2026-08-01/
    *.dmt
    (other Agilent companions)
  sample_B_2026-08-01/
    …
```

Do not flatten only the `.dmt` away from its companions unless you know the reader still finds everything it needs.

`inputs/` is **gitignored** — session data stays on the lab machine.

### 2. Run analysis

```bash
python scripts/batch_morphology_analysis.py
```

Press Enter to use `inputs/`, or type another path.  
Non-interactive:

```bash
python scripts/batch_morphology_analysis.py --non-interactive
```

### 3. Review outputs

Open `outputs/simplified_particle_results.csv` in Excel or your usual editor.

Optional summary:

```bash
python scripts/analyze_results.py
```

`outputs/` is **gitignored**. Archive important CSVs to shared lab storage if needed — not into git.

### 4. Next session

Clear or archive previous folders under `inputs/` / `outputs/` as your lab SOP requires, then drop the next batch into `inputs/`.

## Need more detail?

- CLI flags and algorithm: [batch-morphology.md](batch-morphology.md)
- Column meanings: [../reference/csv-contracts.md](../reference/csv-contracts.md)
- What belongs where: [../reference/inputs-and-outputs.md](../reference/inputs-and-outputs.md)
