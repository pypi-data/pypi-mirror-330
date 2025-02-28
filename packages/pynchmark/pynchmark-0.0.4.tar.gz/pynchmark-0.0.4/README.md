# Pynchmark

Benchmarking tool for Python


## Usage

### Installation

```
pip install pynchmark
```

### Automatic benchmark detection:

Benchmark is automatically detected by adding `, <benchmark_name>` next to the instruction, e.g.:


In `my_bench.py`:
```
import time


def benchmark_fun():

    time.sleep(1), "sleep1_bench"
    time.sleep(3), "sleep3_bench"

```

Then start benchmarks with:
```
$ pynchmark -f my_bench.py -b benchmark_fun -o results.csv
```

Will produce a `results.csv` file with:
```
          name,         time,          std,         cpus
  sleep1_bench,  1.000111500,  0.000390357,  0.548985640
  sleep3_bench,  3.000197003,  0.000279660,  0.150146124
```


### Benchmark parameters:

To run the same benchmark with different values for one or more parameters:

In `my_bench.py`:
```
impott time
import pynchmark as pm


def benchmark_fun():

    for sleep_base in [0.1, 1, 10]:
        for sleep_number in [1, 2, 3]:

            pm.register_param(s=sleep_base, N=sleep_number)

            time.sleep(sleep_base*sleep_number), "sleep"
```

Then
```
$ pynchmark -f my_bench.py -b benchmark_fun
```

Will produce a `results.csv` file with:
```
   name,            s,  N,         time,          std,         cpus
  sleep,  0.100000000,  1,  0.100102915,  0.000129869,  0.830591585
  sleep,  0.100000000,  2,  0.200562054,  0.000355461,  0.075892409
  sleep,  0.100000000,  3,  0.300140898,  0.000016944,  0.414318679
  sleep,  1.000000000,  1,  1.000091083,  0.000107180,  0.148655625
  sleep,  1.000000000,  2,  2.000110503,  0.000182770,  0.429045753
  sleep,  1.000000000,  3,  3.000132126,  0.000098863,  0.346322218
  sleep, 10.000000000,  1, 10.000106712,  0.000191457,  0.285163832
  sleep, 10.000000000,  2, 20.000123678,  0.000403156,  0.471588462
  sleep, 10.000000000,  3, 30.000124734,  0.000205935,  0.542562585
```


### Reuse previous benchmark results

Using `-i <results_file>` will load existing results, and only newly defined benchmarks will be run (benchmarks with same name and paramaters will be skipped, unless they have been in error).

For example:
```
$ pynchmark -i old_results.csv -f my_bench.py -b benchmark_fun -o new_results.csv
```


### Compare results

It is possible to compare two benchmark results and get the speedup between an old and a new one:

```
$ pynchmark -i new_benchmark.csv --compare old_benchmark.csv 
```


### Other features (documentation TODO)

- Plotting
- Other functions in the API



