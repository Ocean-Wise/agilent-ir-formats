"""Unit tests for spectral preprocessing helpers."""

import numpy as np

from agilentirformats.agilent_to_python import data_wns
from agilentirformats.calc_pca import cpca
from agilentirformats.spec_process import deriv, proc, smoother


class _FakeReader:
    def __init__(self, wavenumbers, intensities):
        self.wavenumbers = wavenumbers
        self.intensities = intensities


def test_deriv_length_preserved():
    p = np.arange(10, dtype=float)
    out = deriv(p, 2)
    assert out.shape == p.shape


def test_smoother_odd_window():
    p = np.sin(np.linspace(0, 4, 51))
    out = smoother(p, 5, 2)
    assert out.shape == p.shape


def test_proc_returns_library_length_spectrum():
    data_wavenos = np.linspace(900, 3700, 200)
    library_wavenos = np.linspace(900, 3700, 100)
    spectrum = np.sin(np.linspace(0, 12, 200)) + 0.1
    # proc uses smoother(..., 1001, 2) — needs long enough arrays; pad spectrum/axis
    data_wavenos = np.linspace(900, 3700, 1200)
    spectrum = np.sin(np.linspace(0, 20, 1200)) + 0.1
    out = proc(spectrum, 5, 2, data_wavenos, library_wavenos)
    assert out.shape[0] == library_wavenos.shape[0]


def test_cpca_returns_requested_components():
    rng = np.random.default_rng(0)
    spectra = rng.normal(size=(20, 30))
    comps = cpca(spectra, range(1))
    assert len(comps) == 1
    assert comps[0].shape[0] == 30


def test_data_wns_excludes_co2_band():
    wavenumbers = np.array([800.0, 950.0, 2350.0, 2500.0])
    intensities = np.zeros((2, 2, 4))
    filtered = data_wns(_FakeReader(wavenumbers, intensities))
    assert 2350.0 not in filtered
    assert 800.0 not in filtered  # below 900
    assert 950.0 in filtered
    assert 2500.0 in filtered
