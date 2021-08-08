import numpy as np
import pandas as pd
import operator
import struct
from timeit import default_timer as timer
import concurrent.futures
from multiprocessing import cpu_count

def read_dataset(dataset_filename : str):
    keyset = np.fromfile("../data/" + dataset_filename, dtype=np.uint64)[1:]
    print("Length of keyset: ", len(keyset))
    rankset = rankdata(keyset)
    keyset = keyset.reshape(-1, 1)
    return (keyset, rankset)

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

# Extract non-occupied keys for a given sequence of legitimate and poisoning keys
def partition_non_occupied_keys(K, P):
    keyset = np.append(K, list(P))
    keyset = np.sort(keyset)
    
    n = keyset.shape[0]
    
    lower_bound = int(keyset[0]-1)
    upper_bound = int(keyset[n-1]+1)
    
    # convert to set to speed up lookup
    keyset = set(keyset)
    
    endpoints = []
    is_in_sequence = False
    for i in range(lower_bound, upper_bound + 1):
        # TODO: We limit the number of endpoints to improve performance
        if len(endpoints) > 100:
            return  np.array(endpoints)
        elif (i not in keyset and is_in_sequence is False): # if key i is at start of sequence
            #print("Adding " + str(i) + " to non_occupied_keys")
            is_in_sequence = True
            endpoints.append(i)
        elif i not in keyset and is_in_sequence is True and (i+1) in keyset: # if key i is at end of sequence
            #print("Adding " + str(i) + " to non_occupied_keys because " + str(i+1) + " is not in keyset")
            endpoints.append(i)
        else: 
            is_in_sequence = False
        
    return np.array(endpoints)

# Compute the rank that key S(i) would have if it was inserted in K ∪ P and assign this rank as the i-th element of the new sequence
def compute_rank_for_endpoints(endpoints, keyset):
    computed_rank_for_endpoint = []
    
    for endpoint in endpoints:
        keyset_extended = np.append(keyset, endpoint)
        
        rank = rankdata(keyset_extended)
        
        # extract rank for the last element in the list (the endpoint)
        rank_of_endpoint = rank[len(rank) - 1]
        computed_rank_for_endpoint.append(int(rank_of_endpoint))
    
    return computed_rank_for_endpoint


def obtain_poisoning_keys(p, keyset, rankset):
    # Total number of elements
    n = keyset.shape[0]

    # Number of posoning keys P
    P = int(p * n)
    poisoning_keys = set()
    

    for j in range(P):
        print("Current status: " + str(j) + " out of " + str(P) + " poisoning keys generated")
        # Partition the non-occupied keys into subsequences such that each subsequence consists of consecutive non-occupied keys;
        # Extract the endpoints of each subsequence and sort them to construct the new sequence of endpoints S(i), where i <= 2(n + j);
        
        # S: endpoints
        S = partition_non_occupied_keys(keyset, poisoning_keys)
        #print("Length of endpoints: ", len(S))
        
        # TODO: Investigate impact - we downsample the list of endpoints to max n = 1000
        # Limit number of endpoints to n = 50
        S = np.random.choice(S, size = 50)

        # Compute the rank that key S(i) would have if it was inserted in K ∪ P and assign this rank as the i-th element of the new sequence T (i), where i <= 2(n + j) ;
        # T: list_rank
        T = compute_rank_for_endpoints(S, keyset)

        # Compute the effect of choosing S(1) as a poisoning key and inserting it to K ∪ P with the appropriate rank adjustments. 
        # Specifically, evaluate the sequences each of which is the mean M for a different variable, e.g., K, R, KR. Compute MK (1), MK2 (1), MKR(1), and L(1) ;

        
        delta_S = {}
        M_K = {}
        M_K_square = {}
        M_R = {}
        M_R_square = {}
        M_KR = {}
        L = {}
        
        # Calculate M_K(1), M_R(1) etc.
        # insert first potential poisoning key
        current_keyset = np.append(keyset, S[0])
        M_K[0] = np.mean(current_keyset)

        current_rankset = np.append(rankset, T[0])
        M_R[0] = np.mean(current_rankset)

        M_K_square[0] = np.mean(current_keyset**2)

        M_R_square[0] = np.mean(current_rankset**2)

        M_KR[0] = np.mean(current_keyset*current_rankset)

        nominator = (M_KR[0] - (M_K[0] * M_R[0]))**2
        denominator = M_K_square[0] - (M_K[0])**2
        L[0] = - (nominator / denominator) + M_R_square[0] - (M_R[0])**2

        for i in range(1, len(S)-1):
            # Calculate M_K(i), M_R(i) etc.
            delta_S[i] = S[i+1] - S[i] 

            M_K[i] = M_K[i-1] + delta_S[i] / (n) 
            M_K_square[i] = M_K_square[i-1] + (( 2 * S[i] + delta_S[i]) * delta_S[i]) / (n + 1) 

            M_R[i] = (n + 2) / 2
            M_R_square[i] = ((n+2)*(2*n+3)) / 6
            M_KR[i] = M_KR[i-1] + ( T[i-1] * delta_S[i]) / (n + 1)

            nominator = (M_KR[i] - M_K[i]*M_R[i])**2
            denominator = M_K_square[i] - (M_K[i])**2
            L[i] = - (nominator / denominator) + M_R_square[i] - (M_R[i])**2

        # get argmax of items in L
        optimal_key_index = max(L.items(), key=operator.itemgetter(1))[0]
        
        poisoning_keys.add(S[optimal_key_index])
    
    return poisoning_keys

def perform_poisoning(dataset_filename : str, poisoning_percentage):

    # the SOSD benchmark datasets are already sorted
    x, y = read_dataset(dataset_filename)

    num_processes = cpu_count()
    
    # split x, y into equal parts
    x_split = np.split(x, num_processes)
    y_split = np.split(y, num_processes)

    start = timer()

    futures = []

    with concurrent.futures.ProcessPoolExecutor() as executor:

        for i in range(num_processes):
            future = executor.submit(obtain_poisoning_keys, p = poisoning_percentage, keyset = x_split[i], rankset = y_split[i])
            futures.append(future)


    # obtain poisoning keys
    poisoning_keys = []
    for future in futures:
        result = future.result()
        poisoning_keys.extend(result)

    #x, y = read_dataset(dataset_filename)
    print("Length of legitimate key set: ", len(x))
    print(np.ravel(x))
    print("Length of poisoned key set: ", len(poisoning_keys))
    print(poisoning_keys)
    
    # concat legitimate keys and poisoning keys
    x_poisoned = []
    x_poisoned.extend(np.ravel(x))
    x_poisoned.extend(poisoning_keys)
    x_poisoned.sort()
    x_poisoned = np.array(x_poisoned, dtype=np.uint64)
    print(x_poisoned)

    #y_poisoned = rankdata(x_poisoned)
    
    with open("../data/poisoned_" + dataset_filename + "_" + str(poisoning_percentage), "wb") as output_file:
        output_file.write(struct.pack("Q", len(x_poisoned)))
        x_poisoned.tofile(output_file)
    print("Wrote poisoned dataset poisoned_" + str(dataset_filename) + "_" + str(poisoning_percentage) + " to disk")
    
    end = timer()
    print(f'Elapsed time: {end - start}')

def main():
    # generate 20k poisoning keys (25 cores - 800 keys each)
    #perform_poisoning("wiki_ts_200M_uint64", 0.0001)
    perform_poisoning("wiki_ts_1M_uint64", 0.01)

    #perform_poisoning("osm_cellids_200M_uint64", 0.0001)
    #perform_poisoning("fb_200M_uint64", 0.0001)
    #perform_poisoning("books_200M_uint64", 0.0001)


if __name__ == '__main__':
    main()


