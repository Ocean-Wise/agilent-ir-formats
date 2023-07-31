# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 11:11:13 2020

@author: Shreyas
"""
#import numpy as np
import pandas as pd

import numpy as np
from scipy.signal import savgol_filter as sgf

def deriv(p, w):
    return p - np.roll(p,w)

def hsi_df(data):
    
    wavenumbers = data.wavenumbers
    wn_excluder = np.where(((wavenumbers > 2400) | (wavenumbers < 2300)) 
                           & (wavenumbers >900))[0]
    wn_excl_data = data.intensities[:,:,wn_excluder]
    wns_excl = wavenumbers[wn_excluder]



    hsi_array_rs = wn_excl_data#.reshape(len(wns_excl),4096).transpose()

    return hsi_array_rs

def data_wns(data):
        wavenumbers = data.wavenumbers
        wn_excluder = np.where(((wavenumbers > 2400) | (wavenumbers < 2300)) 
                            & (wavenumbers >900))[0]
        wns_excl = wavenumbers[wn_excluder]
        return wns_excl
