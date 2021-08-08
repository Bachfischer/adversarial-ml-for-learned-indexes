import numpy as np
import pandas as pd
import struct


def read_dataset(dataset_filename : str):
    keyset = np.fromfile("../data/" + dataset_filename, dtype=np.uint64)
    print("Length of keyset: ", len(keyset))
    rankset = rankdata(keyset)
    keyset = keyset.reshape(-1, 1)
    return (keyset, rankset)

def sort_dataset(dataset_filename : str):
    keyset = np.fromfile(dataset_filename, dtype=np.uint64)[1:]
    print("Length of keyset: ", len(keyset))
    keyset_sorted = np.sort(keyset, kind = 'mergesort')

    with open(dataset_filename, "wb") as output_file:
        output_file.write(struct.pack("Q", len(keyset_sorted)))
        keyset_sorted.tofile(output_file)
    
    print("Wrote poisoned dataset " + str(dataset_filename) + " to disk")

"""
Source: Scipy - https://github.com/scipy/scipy/blob/v1.7.0/scipy/stats/stats.py#L8631-L8737
"""
def rankdata(array):
    #arr = np.ravel(np.asarray(array))
    algo = 'mergesort'
    sorter = np.argsort(array, kind=algo)

    inv = np.empty(sorter.size, dtype=np.intp)
    inv[sorter] = np.arange(sorter.size, dtype=np.intp)
    return inv + 1

sort_dataset("../data/poisoned_wiki_ts_200M_uint64")