"""Open Specy / cluster library helpers for polymer identification."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from agilentirformats.paths import (
    DEFAULT_CLUSTER_INDEX,
    DEFAULT_FTIR_METADATA,
    DEFAULT_OS_LIBRARY_DERINT,
    DEFAULT_OS_LIBRARY_INT,
)


@lru_cache(maxsize=1)
def _load_tables(
    metadata_path: str,
    derint_path: str,
    int_path: str,
    index_path: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, np.ndarray]:
    os_meta = pd.read_csv(metadata_path)
    os_meta = os_meta.rename(columns={"sample_name": "particle_ID"})
    os_der_sps = pd.read_csv(derint_path)
    os_sps = pd.read_csv(int_path)
    os_meta_ix = pd.read_csv(index_path)
    os_der_values = os_der_sps.iloc[:, 1:].values
    return os_meta, os_der_sps, os_sps, os_meta_ix, os_der_values


def _tables(
    metadata_path: Path | None = None,
    derint_path: Path | None = None,
    int_path: Path | None = None,
    index_path: Path | None = None,
):
    return _load_tables(
        str(metadata_path or DEFAULT_FTIR_METADATA),
        str(derint_path or DEFAULT_OS_LIBRARY_DERINT),
        str(int_path or DEFAULT_OS_LIBRARY_INT),
        str(index_path or DEFAULT_CLUSTER_INDEX),
    )


def get_lib_wns(y: int = 10) -> np.ndarray:
    """Return library wavenumber axis from the DERINT Open Specy table."""
    _, os_der_sps, _, _, _ = _tables()
    return os_der_sps["wavenos"].values


def norm_pearson(p, q) -> float:
    modp = p / (np.max(p) - np.min(p))
    modq = q / (np.max(q) - np.min(q))
    return stats.pearsonr(modp, modq)[0]


def get_spec(name: str):
    _, _, os_sps, _, _ = _tables()
    return os_sps.loc[:, name]


def catID(k: int) -> str:
    """Map a cluster library index to a simplified polymer name."""
    _, _, _, os_meta_ix, _ = _tables()
    matches = os_meta_ix[os_meta_ix["index"] == k]["simplified_names"]
    if len(matches) == 0:
        return "unknown polymer"
    return matches.values[0]


def pearson_rs(p) -> np.ndarray:
    _, _, _, _, os_der_values = _tables()

    def normp_pearson(q):
        return norm_pearson(p, q)

    return np.apply_along_axis(normp_pearson, axis=0, arr=os_der_values)


def libOS_fit_1(p) -> pd.DataFrame:
    os_meta, _, _, _, _ = _tables()
    sorter_df = pd.concat(
        [
            os_meta[["spectrum_identity", "particle_ID", "clust_ix"]],
            pd.Series(pearson_rs(p), name="Pearson_Rs"),
        ],
        axis=1,
        sort=False,
    )
    return sorter_df.sort_values(by=["Pearson_Rs"], ascending=False)[:5]
