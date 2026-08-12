# 2026-08-12 — Repository scaffold for lab use

## What changed

- Introduced `inputs/` and `outputs/` (gitignored) as the default session I/O locations.
- Moved installable code under `src/agilentirformats/`, lab CLIs under `scripts/`, notebooks under `notebooks/`.
- Moved polymer / Open Specy libraries to `data/libraries/`; sample CSVs to `data/fixtures/`.
- Batch morphology defaults no longer point at a hard-coded Windows Downloads path.
- Added `AGENTS.md`, `CONTRIBUTING.md` (PR workflow), and docs under `docs/`.

## Why

Support repeated FTIR sample sessions for Stephanie Wang and other technicians without committing raw scans or scattering scripts at the repo root.
