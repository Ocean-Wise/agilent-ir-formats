# Inputs and outputs

## `inputs/` (gitignored)

**Purpose:** Incoming Agilent FTIR project data for the current (or queued) analysis sessions.

**Put here:**

- Project folders from the instrument / shared drive
- `.dmt` (and `.seq`) files with their companion files kept together

**Do not put here:**

- Final reviewed CSVs you want to keep forever (archive elsewhere; optional copy under lab storage)
- Edits to polymer libraries (those belong in `data/libraries/` via a PR)

Default CLI path for batch morphology: `inputs/`.

## `outputs/` (gitignored)

**Purpose:** Everything the tools generate for a session.

**Put here / written here:**

- `simplified_particle_results.csv` (default batch output)
- Campaign-named CSVs (`--output outputs/campaign_name.csv`)
- Optional plots or intermediate exports you generate while reviewing

**Do not commit** these files. If a small example is needed for docs or tests, copy a trimmed CSV into `data/fixtures/` in a PR.

## `data/libraries/` (tracked)

Reference spectra and cluster tables required for polymer matching. Changing these is a scientific decision — use a PR and note it in `docs/changes/`.

## `data/fixtures/` (tracked)

Small, safe example CSVs for documentation and automated tests. Not a substitute for real session archives.
