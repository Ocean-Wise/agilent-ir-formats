# Batch morphology + spectroscopy

Automates particle segmentation and polymer identification from Agilent hyperspectral `.dmt` files.

## Inputs

| Input | Location | Required | Notes |
|-------|----------|----------|-------|
| Agilent project(s) | `inputs/` (default) or `--input` | Yes | Recursive search for `*.dmt` |
| Cluster library | `data/libraries/OS_clusters_DERINT.csv` | Yes | Override with `--library` |
| Open Specy DERINT + index | `data/libraries/` | Yes | Used for wavenumbers + `catID` names |

Place **whole project folders** under `inputs/`. The tool walks subdirectories for every `.dmt`.

## Outputs

| Output | Default path | Description |
|--------|--------------|-------------|
| Combined particle CSV | `outputs/simplified_particle_results.csv` | One row per particle across all files |

Override with `--output path/to/file.csv`.

### Result columns

See [CSV contracts](../reference/csv-contracts.md#batch-morphology-results).

## Commands

```bash
# Default: read inputs/, write outputs/simplified_particle_results.csv
python scripts/batch_morphology_analysis.py --non-interactive

# Single file
python scripts/batch_morphology_analysis.py --input path/to/file.dmt

# Custom paths
python scripts/batch_morphology_analysis.py \
  --input inputs/campaign_2026-08 \
  --output outputs/campaign_2026-08.csv \
  --min-pixels 5

# After install (-e .)
agilent-batch-morphology --non-interactive
```

Windows launcher: `scripts\run_analysis.bat`.

## Algorithm (summary)

1. **Load** hyperspectral cube + total absorbance image via `AgilentIRFile`
2. **Threshold** `mean(image) + 2 * std(image)`
3. **Segment** connected components (`skimage.measure.label` / `regionprops`)
4. **Reduce** each particle’s spectra with PCA (`calc_pca.cpca`)
5. **Process** spectrum (background, interpolate to library axis, smooth, derivative)
6. **Match** against cluster library (correlation); name via `library_OS_fit.catID`
7. **Area** from pixel count × `(fpasize µm)²` (default 64 µm if metadata missing)

Confidence: `best_pr < 0.3` → polymer name tagged `(low confidence)`.

## Related scripts

| Script | Role |
|--------|------|
| `scripts/batch_morphology_analysis.py` | Batch runner |
| `scripts/analyze_results.py` | Print polymer / confidence summary |
| `scripts/legacy/*` | Historical patches — not part of the lab SOP |
