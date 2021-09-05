Connection to SOSD Benchmark Server (with n= 8 CPUs, e2-standard-8):

ssh -i .ssh/google_compute_engine bachfischer@130.211.197.90

SSH access to GitHub:
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/sosd_benchmark
git pull

Configuration for SOSD Benchmark: e2-standard-8
Configuration for SOSD Benchmark (LIPP-only): e2-standard-16 

Configuration for Poisoning attack: c2-standard-30

Query benchmark:
`./build/benchmark -r 1 ./data/books_200M_uint64 ./data/books_200M_uint64_equality_lookups_10M --pareto --only ALEX`

Insertion benchmark:
`./build/benchmark -r 1 ./data/books_200M_uint64 ./data/books_200M_uint64_equality_lookups_18M --inserts ./data/books_200M_uint64_inserts_2M --pareto --only DPGM`

Note:

Running SOSD benchmark requires at least 32GB of RAM (see https://github.com/learnedsystems/SOSD/issues/9)


In terms of performance, ALEX has a couple of known limitations:

# Attack 1:

The premise of ALEX is to model the key distribution using a collection of linear regressions. Therefore, ALEX performs poorly when the key distribution is difficult to model with linear regressions, i.e., when the key distribution is highly nonlinear at small scales. A possible future research direction is to use a broader class of modeling techniques (e.g., also consider polynomial regression models).

## Out-of-box dataset from ALEX authors
./build/benchmark \
--keys_file=/data/longitudes-200M.bin \
--keys_file_type=binary \
--init_num_keys=10000000 \
--total_num_keys=20000000 \
--batch_size=1000000 \
--insert_frac=0.5 \
--lookup_distribution=zipf \
--print_batch_stats

## Random Dataset (Size: 2000 keys)

#### Custom dataset (random)
./build/benchmark \
--keys_file=/data/random_2000.csv \
--keys_file_type=text \
--init_num_keys=1000 \
--total_num_keys=2000 \
--batch_size=500 \
--insert_frac=0.5 \
--lookup_distribution=uniform \
--print_batch_stats

Cumulative stats: 5 batches, 2250 ops (1250 lookups, 1000 inserts)
cumulative throughput:	1.420e+07 lookups/sec,	1.111e+04 inserts/sec,	2.496e+04 ops/sec

#### Custom dataset (poisoned)

./build/benchmark \
--keys_file=/data/poisoned_keyset_2000.csv \
--keys_file_type=text \
--init_num_keys=1000 \
--total_num_keys=2401 \
--batch_size=500 \
--insert_frac=0.5 \
--lookup_distribution=uniform \
--print_batch_stats

Cumulative stats: 6 batches, 2901 ops (1500 lookups, 1401 inserts)
cumulative throughput:	1.012e+07 lookups/sec,	1.098e+04 inserts/sec,	2.270e+04 ops/sec

## Random Dataset (Size: 5000 keys)

#### Custom dataset (random)
./build/benchmark \
--keys_file=/data/random_5000.csv \
--keys_file_type=text \
--init_num_keys=2500 \
--total_num_keys=5000 \
--batch_size=1000 \
--insert_frac=0.5 \
--lookup_distribution=uniform \
--print_batch_stats

Cumulative stats: 6 batches, 5500 ops (3000 lookups, 2500 inserts)
cumulative throughput:	5.104e+06 lookups/sec,	7.104e+03 inserts/sec,	1.560e+04 ops/sec

#### Custom dataset (poisoned)

./build/benchmark \
--keys_file=/data/poisoned_keyset_5000.csv \
--keys_file_type=text \
--init_num_keys=2500 \
--total_num_keys=5251 \
--batch_size=1000 \
--insert_frac=0.5 \
--lookup_distribution=uniform \
--print_batch_stats

Cumulative stats: 6 batches, 5751 ops (3000 lookups, 2751 inserts)
cumulative throughput:	5.295e+06 lookups/sec,	1.237e+04 inserts/sec,	2.579e+04 ops/sec

## Wiki Dataset

#### Custom dataset (random)
./build/benchmark \
--keys_file=/data/wiki_ts_1M_uint64 \
--keys_file_type=binary \
--init_num_keys=12207 \
--total_num_keys=24415 \
--batch_size=5000 \
--insert_frac=0.5 \
--lookup_distribution=uniform \
--print_batch_stats

Cumulative stats: 5 batches, 24708 ops (12500 lookups, 12208 inserts)
cumulative throughput:	1.929e+06 lookups/sec,	1.884e+04 inserts/sec,	3.776e+04 ops/sec
(base) bachfischer

#### Custom dataset (poisoned)

./build/benchmark \
--keys_file=/data/poisoned_wiki_ts_1M_uint64_0.2 \
--keys_file_type=binary \
--init_num_keys=12207 \
--total_num_keys=24415 \
--batch_size=5000 \
--insert_frac=0.5 \
--lookup_distribution=uniform \
--print_batch_stats

Cumulative stats: 5 batches, 24708 ops (12500 lookups, 12208 inserts)
cumulative throughput:	1.837e+06 lookups/sec,	1.831e+04 inserts/sec,	3.667e+04 ops/sec

# Attack 2:

ALEX can have poor performance in the presence of extreme outlier keys, which can cause the key domain and ALEX's tree depth to become unnecessarily large (see Section 5.1 of our paper). A possible future research direction is to add special logic for handling extreme outliers, or to have a modeling strategy that is robust to sparse key spaces.


Code: https://github.com/umatin/LogarithmicErrorRegression/blob/9ff3aae3862586dd894be3f6caea897adcc00373/src/helpers/io_handler.h