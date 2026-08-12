# Contributing

Thanks for helping keep this FTIR lab tooling reliable for Stephanie and other technicians.

## The golden rule

> **`main` is always usable.** Every merge must leave docs, defaults, and scripts in a coherent state.

**Do not commit or push directly to `main`.** All changes go through a pull request.

## Quick workflow

```bash
git checkout main && git pull
git checkout -b feat/short-description

# make changes, update docs (see AGENTS.md checklist)
pip install -e ".[dev]"
pytest

git add -A
git commit -m "feat: describe why this change helps the lab"
git push -u origin HEAD
gh pr create   # or open a PR in the GitHub UI
```

After review: **squash and merge**, then delete the branch.

## Branch naming

| Prefix | Use for |
|--------|---------|
| `feat/` | New capability |
| `fix/` | Bug fix |
| `docs/` | Documentation only |
| `chore/` | Tooling, deps, scaffolding |
| `refactor/` | Internal restructuring |

## What a good PR includes

1. **Focused scope** — one logical change when practical.
2. **Docs** — guides/reference updated if behaviour or I/O changed ([AGENTS.md](AGENTS.md)).
3. **No session data** — nothing from `inputs/` or `outputs/`.
4. **Test plan** — how a technician or reviewer can verify (even if manual).

Use this PR body shape:

```markdown
## Summary
- …

## Problem Statement
…

## Solution
…

## Key Changes
- …

## Testing
- [ ] …

## Risks
- …

## Follow-ups
- …
```

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Checks before push (same as PR CI)

```bash
ruff check src scripts tests
pytest -q
python scripts/batch_morphology_analysis.py --help
python scripts/analyze_results.py --help
```

GitHub runs these on every pull request via [`.github/workflows/pr.yml`](.github/workflows/pr.yml) (Python 3.10 and 3.12).

## Documentation expectations

- Lab procedures → `docs/guides/`
- Contracts / structure → `docs/reference/`
- Notable behaviour changes → dated file in `docs/changes/`
- Agent rules → `AGENTS.md` (update when folder rules change)

## Questions

If unsure where a file belongs, see [docs/reference/folder-structure.md](docs/reference/folder-structure.md) or ask before adding a new top-level directory.
