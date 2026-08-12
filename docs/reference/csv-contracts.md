# CSV contracts

## Batch morphology results

Default file: `outputs/simplified_particle_results.csv`  
Fixture example: `data/fixtures/simplified_particle_results_with_area.csv` (may include extra columns from older runs)

| Column | Type | Description |
|--------|------|-------------|
| `fileID` | string | Source `.dmt` file name |
| `label` | int | Particle ID within that file |
| `polymer` | string | Identified polymer (may include `(low confidence)`) or `small particle` / `error` |
| `best_pr` | float | Match confidence score (correlation; typically 0–1) |
| `pixel_count` | int | Pixels in the particle mask |
| `area_mm2` | float | Physical area in mm² |

Older notebooks may also emit `dmt_file`, `area_um2`, or `error` — treat those as optional/legacy unless the batch CLI is updated and this table is revised.

## Cluster library

`data/libraries/OS_clusters_DERINT.csv` — spectra matrix used for matching (transposed on load).  
`data/libraries/OS_cluster_index.csv` — maps cluster `index` → `simplified_names` via `catID`.

## Open Specy libraries

| File | Role |
|------|------|
| `open_specy_ftir_library_DERINT.csv` | Derivative-intensity library + `wavenos` axis |
| `open_specy_ftir_library_INT.csv` | Intensity library |
| `ftir_metadata_clusters.csv` | Metadata for library entries |
| `open_specy_ftir_metadata.csv` | Additional Open Specy metadata |

When columns or naming conventions change, update this file and add a note under `docs/changes/`.
