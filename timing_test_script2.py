from agilent_ir_file import AgilentIRFile
import spec_process as spec_p
import numpy as np
from scipy import stats
import agilent_to_python as a2p
import library_OS_fit as lib_OS
import pandas as pd

filename = r'C:\Users\Shreyas.Patankar\Ocean Wise Conservation Association\Plastics Lab Team - General\00_FTIR_Data\mosaic_test_and_results\m3\m3.dmt'
clust_der_values = pd.read_csv('OS_clusters_DERINT.csv')
reader = AgilentIRFile()
reader.read(filename)

library_wavenos = lib_OS.get_lib_wns()

smoothing_order = 1
smoothing_window = 5

wavenumbers = a2p.data_wns(reader)


intensities = a2p.hsi_df(reader)

def norm_pearson(p,q):
    modp = p/(np.max(p) - np.min(p))
    modq = q/(np.max(q) - np.min(q))
    return stats.pearsonr(modp,modq)[0]


def pearson_rs(p):
    def normp_pearson(q):
        return norm_pearson(p,q)
    return np.apply_along_axis(normp_pearson,axis=0,arr=clust_der_values)

proc = spec_p.proc(intensities[-219,154,:],smoothing_window, smoothing_order,wavenumbers,library_wavenos)

import time



def bPR0(p):
    proc = spec_p.proc(p,smoothing_window, smoothing_order,wavenumbers,library_wavenos)
    prsc = pearson_rs(proc)
    ix = np.argmax(prsc)
    if prsc[ix] > 0.3:
        return ix 
    else: return 0

llim = 300


#print(list(np.argwhere(reader.total_image > llim)))
ll = [tuple(k) for k in np.argwhere(reader.total_image > llim)]

rows = [k[0] for k in ll]
cols = [k[1] for k in ll]
idmap = np.zeros_like(reader.total_image)


from multiprocessing import Pool

pool = Pool(processes=6)

start = time.time()
#maplist = pool.map(bPR0,[intensities[k] for k in ll])
#idmap[rows,cols] = list(maplist)


# protect the entry point
if __name__ == '__main__':
    # create and configure the process pool
    with Pool() as pool:
        # execute tasks in order
        for result in pool.map(bPR0,[intensities[k] for k in ll]):
            print(f'Got result: {result}', flush=True)
    # process pool is closed automatically
end = time.time()
print('eval time bPR map multicore= ', end - start)