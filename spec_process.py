import numpy as np
from scipy.signal import savgol_filter as sgf

def deriv(p, w):
    deriv_a = np.array(p) - np.roll(p,w)
    deriv_a[:w] = deriv_a[w]
    return deriv_a

def smoother(p, smoothing_window, smoothing_order):

        return np.array(sgf(p,smoothing_window,smoothing_order))

def bgF(p):
    return np.array(p)-np.array(smoother(p,1001,2))

def proc(p, smoothing_window, smoothing_order, data_wavenos, library_wavenos):
    p_bgF = (np.array(p)-np.array(smoother(p,1001,2))) 
    p_int = np.interp(library_wavenos,data_wavenos[20:],p_bgF[20:]) 
    p_smt = sgf(p_int, smoothing_window, smoothing_order) 
    p_der = deriv(p_smt,2)
    pnoise = p_der-smoother(p_der,smoothing_window, smoothing_order)
    p_der[np.abs(pnoise)>np.std(pnoise)] = 0
    return p_der