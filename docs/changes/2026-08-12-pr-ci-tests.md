# 2026-08-12 — PR CI and expanded tests

## What changed

- Added `.github/workflows/pr.yml` (ruff, pytest, script `--help` on Python 3.10 / 3.12).
- Expanded `tests/` to cover batch CLI helpers, preprocessing, analyze-results, and script entrypoints.
- Documented the local pre-push command set in `AGENTS.md` / `CONTRIBUTING.md`.

## Why

Catch script and package regressions before merge, matching Ocean Wise PR-check practice.
