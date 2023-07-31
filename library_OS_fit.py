import pandas as pd
import os
import numpy as np
from scipy import stats

OS_meta = pd.read_csv('ftir_metadata_clusters.csv')
OS_meta.rename(columns={'sample_name':'particle_ID'}, inplace=True)
OS_der_sps = pd.read_csv('open_specy_ftir_library_DERINT.csv')
OS_sps = pd.read_csv('open_specy_ftir_library_INT.csv')
OS_meta_ix = pd.read_csv('OS_cluster_index.csv')

OS_der_values = OS_der_sps.iloc[:,1:].values

def get_lib_wns(y=10):
    return OS_der_sps['wavenos'].values

def norm_pearson(p,q):
    modp = p/(np.max(p) - np.min(p))
    modq = q/(np.max(q) - np.min(q))
    return stats.pearsonr(modp,modq)[0]

def get_spec(name):
    return OS_sps.loc[:,name]

def catID(k):
    return (OS_meta_ix[OS_meta_ix['index'] == k]['simplified_names']).values[0]

def pearson_rs(p):
    def normp_pearson(q):
        return norm_pearson(p,q)
    return np.apply_along_axis(normp_pearson,axis=0,arr=OS_der_values)

def libOS_fit_1(p):
    sorter_df = pd.concat([OS_meta[['spectrum_identity','particle_ID','clust_ix']],
                       pd.Series(pearson_rs(p), name='Pearson_Rs')],
                      axis=1, sort=False)
    sorter_df = (sorter_df.sort_values(by=['Pearson_Rs'], ascending = False))[:5]
    return sorter_df
