#!/bin/bash

# Script to run all benchmarks in all directories
#   - Variables in ALL CAPS can be considered global
#   - Variables in lower case should only be used locally to that function

# Author: Jordan Mata
# Date: Nov 22, 2022

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PACKAGE_DIR="${SCRIPTPATH}"
DATA_DIR="${PACKAGE_DIR}/data"
INPUT_DATA_DIR="${DATA_DIR}/data_to_encrypt"
ENCRYPTED_DATA_DIR="${DATA_DIR}/encrypted_data"
BENCHMARK_DATA_DIR="${DATA_DIR}/benchmark_data"

DATA_FILE=${BENCHMARK_DATA_DIR}/data.csv

# names of the directories in root directory (excluding data/)
ENCRYPTION_ALG_DIR_LIST=($(ls -d ${PACKAGE_DIR}/*/ | grep -v data))

# Sets up anything we need before running the benchmarks
setup() {
    if [[ -f "$DATA_FILE" ]]; then
        echo -e "\nData file already exists! Delete it or rerun it. Filename:\n${DATA_FILE}\n"
        rm $DATA_FILE
    fi
    echo "Algorithm, File_Size, Encrypted_Size, Resident_Size, System_Time, Wall_Clock_Time" > "$DATA_FILE"

    #sudo apt-get install linux-tools-common linux-tools-5.15.0-52-generic
    #sudo sysctl -w kernel.perf_event_paranoid=-1
}

# Writes a single line to our csv with our benchmarking data
# args:
#   See usage statement
record_data() {
    if [[ $# != 6 ]]; then
        echo -e "\nError with parse_output(alg_name, data_file_size, encrypted_size, resident_size, system_time, wall_clock_time)"
        echo -e "Received $# input parameters.\n"
        exit -1
    fi

    alg_name=$1
    data_file_size=$2
    resident_size=$3
    system_time=$4
    wall_clock_time=$5

    echo "$alg_name, $data_file_size, $encrypted_size, $resident_size, $system_time, $wall_clock_time" >> "$DATA_FILE"
}


# Parses the output of "time" and extracts the resident size, wall time, and system time.
#
# args:
#   1. the "time" output stored in a variable
# Side effect:
#   - populates the RESIDENT_SIZE global variable
#   - populates the SYSTEM_TIME global variable
#   - populates the WALL_CLOCK_TIME global variable
parse_time_output() {
    if [[ $# != 1 ]]; then
        echo -e "\nError with parse_time_output(time_output)"
        echo -e "Received $# input parameters.\n"
        exit -1
    fi
    
    time_output=$1

    # TODO 
    # FIX parsing of times. Grep isn't working correctly. Use regex instead
    RESIDENT_SIZE=$(echo -e "$time_output" | grep "Maximum resident set size (kbytes):" | grep -oE '[0-9]+')
    SYSTEM_TIME=$(echo -e "$time_output" | grep "System time (seconds):" | grep -oE '[0-9]+.[0-9]+')
    WALL_CLOCK_TIME=$(echo -e "$time_output" | grep "Elapsed (wall clock) time (h:mm:ss or m:ss):" | grep -oE '[0-9]+:[0-9]+.[0-9]+')
}


# simple function to iterate over each algorithm and run the benchmark a given number of times
# args:
#   1. iterations - number of times to run each algorithm on each data input
run_all_algorithms_encryption() {
    iterations=$1
    for algorithm_dir in ${ENCRYPTION_ALG_DIR_LIST[@]}; do
        run_encryption_on_algorithm "$algorithm_dir" $iterations
    done
}


# Calls the algorithm run script on the entire set of data files
# and run the benchmark a given number of times
# args:
#   1. alg_dir_name - path to the algorithm
#   2. iterations - number of times to run each algorithm on each data input
run_encryption_on_algorithm() {
    alg_dir_name=$1
    iterations=$2

    alg_name=$(basename $alg_dir_name)
    # script that will do the run for us as long as we give the input parameters
    run_script="${alg_dir_name}/run.sh"

    # encrypt each file in the DATA_DIR.
    for data_filename in $INPUT_DATA_DIR/*; do
        filename_without_ext=$(basename $data_filename .txt)
        # Write encrypted file in ENCRYPTED_DATA_DIR with extension enc
        encrypted_filepath=$ENCRYPTED_DATA_DIR/$filename_without_ext.enc

        for (( i=0; i<$iterations; i++)); do
            echo "Running ${alg_name} iteration $i/$iterations" 
            # call a subscript to time the exe for us, then parse it
            # This part of the line lets us avoid context switches to get more accurate times:
            #   sudo chrt -f 99
            time_output=$(sudo chrt -f 99 /usr/bin/time --verbose \
                            "$run_script" "$data_filename" \
                            "$encrypted_filepath" "$CIPHER_KEY" 2>&1)
            parse_time_output "$time_output"

            # generate other benchmark data
            file_size=$(stat --printf="%s" "$data_filename")
            encrypted_size=$(stat --printf="%s" "$encrypted_filepath")

            # log the data line item
            record_data "$alg_name" "$file_size" "$encrypted_size" "$RESIDENT_SIZE" "$SYSTEM_TIME" "$WALL_CLOCK_TIME"
        done
    done       
}


run_decryption() {
    # this is optional to make sure decryption works
    # decrypt all files in the ENCRYPTED_DATA_DIR folder
    for encrypted_filename in $ENCRYPTED_DATA_DIR/*; do
        filename_without_ext=$(basename $encrypted_filename .enc)
        encrypted_filepath=$ENCRYPTED_DATA_DIR/$filename_without_ext.enc
        
        # This part of the line lets us avoid context switches to get more accurate times
        #   sudo chrt -f 99 /usr/bin/time --verbose
        # The rest is calls the  the algorithm with the specified file as output
        # set as /dev/null since we don't care about the actual output
        sudo chrt -f 99 /usr/bin/time --verbose $EXE decrypt "/dev/null" "$CIPHER_KEY" < $encrypted_filepath
    done
}


# This will call all the scripts we want
main() {
    setup
    run_all_algorithms_encryption 3 # second param is number of times to encrypt each file
}

main # run main()