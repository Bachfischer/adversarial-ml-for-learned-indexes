# adversarial-ml-for-learned-indexes

## Overview

This repository contains experiments for the "Learned Indexes" research project at the University of Melbourne. The project is jointly supervised by Ben Rubinstein and Renata Borovica-Gajic.

## Project structure

* `data/` -- Various datasets
* `doc/` -- Documentation
* `experimental-results/` -- Output from experimental evaluation using [SOSD](https://github.com/Bachfischer/SOSD/tree/develop)
* `src/` -- Source code for experiments

## System configuration

Configuration for SOSD Benchmark: *e2-standard-8* 

Configuration for SOSD Benchmark (LIPP-only): *e2-standard-16* 

Configuration for Poisoning attack: *c2-standard-30*

Note: Running SOSD benchmark requires at least 32GB of RAM (see https://github.com/learnedsystems/SOSD/issues/9)

## Cheatsheet

Connection to SOSD Benchmark server (with n=8 CPUs, e2-standard-8):

```
ssh -i .ssh/google_compute_engine bachfischer@130.211.197.90
```

SSH access to GitHub on SOSD Benchmark server:
```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/sosd_benchmark
git pull
```

Query benchmark:
```
./build/benchmark -r 1 ./data/books_200M_uint64 ./data/books_200M_uint64_equality_lookups_10M --pareto --only ALEX
```

Insertion benchmark:
```
./build/benchmark -r 1 ./data/books_200M_uint64 ./data/books_200M_uint64_equality_lookups_18M --inserts ./data/books_200M_uint64_inserts_2M --pareto --only DPGM
```

## Contact

For more information, please feel free to contact me via e-mail ([bachfischer.matthias@googlemail.com](mailto:bachfischer.matthias@googlemail.com)) 