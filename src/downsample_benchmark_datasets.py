import numpy as np
import struct

from numpy.core.numeric import full

def downsample_dataset(dataset_filename : str, downsample_factor):
    full_keyset = np.fromfile("../data/" + dataset_filename + "_ts_200M_uint64", dtype=np.uint64)[1:]
    print("Length of full keyset: ", len(full_keyset))
    reduced_keyset = np.delete(full_keyset, np.arange(0, full_keyset.size, downsample_factor))
    downsampled_keyset = full_keyset[::downsample_factor]
    print("Length of downsampled keyset: ", len(downsampled_keyset))
    
    with open("../data/" + dataset_filename + "_ts_1M_uint64", "wb") as output_file:
        output_file.write(struct.pack("Q", len(downsampled_keyset)))
        downsampled_keyset.tofile(output_file)

# downsample_factor = 10000 : 5 seconds
# downsample_factor = 1000  : 5 minutes
# downsample_factor = 10    : TBD 
downsample_dataset("wiki", 10)

#downsample_dataset("books", 131072)
#downsample_dataset("osm_cellids", 131072)
#downsample_dataset("fb", 131072)
