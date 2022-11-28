# Multimedia Encryption Research
## Brief
This is a benchmark suite for benchmarking different text based encryption algorithms. The goal is to compare the runtime, max memory usage, and other relevant stats to compare different algorithms objectively.

# Flow of Logic
The user needs to execute `~/run_all_benchmarks.sh` with sudo privileges (see `Use of Sudo` for details on why sudo is needed).</br>
The script will do the following:
```
For alg_dir in algorithm_directories (the root of the package):
    For i in num_iterations:
        For data_file in the ~/data/data_to_encrypt:
            alg_dir/run.sh script is executed with the specified data_file
            parse the data from the execution
            append the parsed data to ~/data/benchmark_data/data.csv 
```

## Adding another algorithm
To add a new algorithm:
1. Create a new folder in the root of the package with the name of the algorithm. (eg `~/AES/`)
2. Place the algorithm implementation in a `src` directory within the folder from (1). (eg. `~/AES/src/`)
3. Create a `run.sh` bash script in the algorithm root (eg. `~/AES/run.sh`). This script should accept `input_file`, `output_file`, and `encryption_key` as input parameters and call the algorithm executable with those parameters.
4. Add the algorithm name to the ENCRYPTION_ALG_LIST variable in the `run_all_benchmarks` script. The algorithm name MUST match the folder name from (1).

# Use of Sudo
1. `chrt` to pin the process with a high priority in the process table to avoid context switches.
2. use of some linux tools that require kernel access to read from some OS data (TODO flesh this explanation out)

## Important Notes
While introducing a `run.sh` script will incur some overhead, each script is minimal and the overhead should be negligible given that the items in the data set are sufficiently large.