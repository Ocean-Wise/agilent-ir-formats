"""Helpers to extract wavenumber-filtered hyperspectral arrays from AgilentIRFile."""

import numpy as np


def deriv(p, w):
    return p - np.roll(p, w)


def hsi_df(data):
    wavenumbers = data.wavenumbers
    wn_excluder = np.where(
        ((wavenumbers > 2400) | (wavenumbers < 2300)) & (wavenumbers > 900)
    )[0]
    wn_excl_data = data.intensities[:, :, wn_excluder]
    return wn_excl_data


def data_wns(data):
    wavenumbers = data.wavenumbers
    wn_excluder = np.where(
        ((wavenumbers > 2400) | (wavenumbers < 2300)) & (wavenumbers > 900)
    )[0]
    return wavenumbers[wn_excluder]
