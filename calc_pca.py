import pandas as pd
from sklearn.decomposition import PCA
from scipy import stats
import numpy as np

def cpca(hsi_spectra, ords):
    #remove outliers

    outlier_margin = 20
    hsi_spectra[hsi_spectra > (np.median(hsi_spectra)+outlier_margin*np.std(hsi_spectra))] = np.mean(hsi_spectra)#+outlier_margin*np.std(hsi_spectra)
    hsi_spectra[hsi_spectra < (np.median(hsi_spectra)-outlier_margin*np.std(hsi_spectra))] = np.mean(hsi_spectra)#-outlier_margin*np.std(hsi_spectra)

    pca = PCA(n_components=5)
    pca.fit(hsi_spectra)
    print('pca calculated')

    pcomponents = [pca.components_[i] for i in ords]
    return pcomponents