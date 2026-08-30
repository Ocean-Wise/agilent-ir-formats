# AGENTS.md — Agent guidance for this repository

Guidance for AI agents and automation working in **agilent-ir-formats**. Follow this file together with [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/reference/folder-structure.md](docs/reference/folder-structure.md).

## Who this repo is for

Lab technicians (primary administrator: **Stephanie Wang**) run FTIR microplastic sessions repeatedly. Prefer durable defaults (`inputs/`, `outputs/`, documented CLIs) over one-off hard-coded machine paths.

## Golden rules

1. **Never push or commit directly to `main`.** Branch → PR → review → squash-merge. See CONTRIBUTING.md.
2. **Do not create commits or PRs unless the user asks.** Draft changes locally; wait for an explicit commit/PR request.
3. **Document as you go.** A code change without matching docs is incomplete.
4. **Respect the folder structure.** Do not dump scripts, CSVs, or notebooks at the repo root.
5. **Never commit session data.** `inputs/` and `outputs/` are gitignored for a reason.

## Required folder map

| Path | Purpose | Git |
|------|---------|-----|
| `src/agilentirformats/` | Installable package (reader + analysis) | tracked |
| `scripts/` | Lab-facing CLIs and Windows launcher | tracked |
| `scripts/legacy/` | One-off patches / timing experiments | tracked |
| `notebooks/` | Exploratory `.ipynb` | tracked |
| `inputs/` | Incoming Agilent projects / `.dmt` sessions | **ignored** (keep README + `.gitkeep`) |
| `outputs/` | Analysis results | **ignored** (keep README + `.gitkeep`) |
| `data/libraries/` | Open Specy + cluster libraries | tracked |
| `data/fixtures/` | Small example CSVs for docs/tests | tracked |
| `docs/guides/` | How-to procedures | tracked |
| `docs/reference/` | Contracts, structure, field maps | tracked |
| `docs/changes/` | Dated notes when behaviour or contracts change | tracked |
| `tests/` | Automated tests | tracked |

## Document-as-you-go checklist

Whenever you change tooling, update the matching docs **in the same change set**:

| If you change… | Also update… |
|----------------|--------------|
| Batch CLI flags, defaults, or algorithm | `docs/guides/batch-morphology.md`, `docs/guides/lab-workflow.md` |
| Result CSV columns | `docs/reference/csv-contracts.md` + fixture examples if shape changed |
| `inputs/` / `outputs/` expectations | `docs/reference/inputs-and-outputs.md`, folder READMEs |
| Package public API (`AgilentIRFile`, exports) | `docs/guides/reading-agilent-files.md`, root `README.md` |
| Folder layout or new top-level dirs | `docs/reference/folder-structure.md`, `AGENTS.md`, `README.md` |
| Behaviour stewards should remember later | New dated note under `docs/changes/` |

Skipping docs leaves Stephanie (and the next agent) unable to run or trust the tool — treat that as a failed change.

## Coding conventions

- Prefer extending `src/agilentirformats/` over adding new root-level modules.
- Resolve paths via `agilentirformats.paths` (repo-root aware). Do **not** hard-code `C:\Users\Stephanie.Wang\...` or similar.
- Default CLI I/O to `inputs/` and `outputs/`.
- Keep lab CLIs runnable both as installed entry points and via `python scripts/...` (scripts may add `src/` to `sys.path` for convenience).
- Leave `scripts/legacy/` alone unless fixing breakage; prefer new scripts under `scripts/` with docs.

## Git / PR behaviour (agent-enforced)

- Branch from `main` using prefixes: `feat/`, `fix/`, `docs/`, `chore/`, `refactor/`.
- Do not force-push to `main`. Do not skip hooks.
- Before assisting with `git push`, run the same checks as `.github/workflows/pr.yml`:

  ```bash
  pip install -e ".[dev]"
  ruff check src scripts tests
  pytest -q
  python scripts/batch_morphology_analysis.py --help
  python scripts/analyze_results.py --help
  ```

  If any required command fails, stop and report before push-related steps.
- PR titles should be conventional commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`).

## Safety

- Do not delete or rewrite `data/libraries/` without an explicit user request and a `docs/changes/` note.
- Do not commit `.env`, credentials, or large raw scan dumps.
- Upstream reader attribution (Alex Henderson / MIT) stays in README, LICENSE, and CITATION.cff.
