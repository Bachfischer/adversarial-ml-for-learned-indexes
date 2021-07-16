import numpy as np
import struct

def downsample_dataset(dataset_filename : str, downsample_factor):
    full_keyset = np.fromfile("../data/" + dataset_filename + "_ts_200M_uint64", dtype=np.uint64)[1:]
    reduced_keyset = np.delete(full_keyset, np.arange(0, full_keyset.size, downsample_factor))
    downsampled_keyset = full_keyset[::downsample_factor]
    print("Length of downsampled keyset: ", len(downsampled_keyset))
    
    with open("../data/" + dataset_filename + "_ts_1M_uint64", "wb") as output_file:
        output_file.write(struct.pack("Q", len(downsampled_keyset)))
        downsampled_keyset.tofile(output_file)

downsample_dataset("wiki", 8192)
#downsample_dataset("books", 131072)
#downsample_dataset("osm_cellids", 131072)
#downsample_dataset("fb", 131072)
