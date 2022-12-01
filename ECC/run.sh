#!/bin/bash

# Subscript meant to run the encryption algorithm for us.
# Lets us decouple the input parameters and order at the cost of
# slight overhead in time/complexity. THis should be negligible.
# 
# args:
#   1. input file (file to encrypt)
#   2. output file (file to decrypt)
#   3. cipher key (optional)

# [program source](https://github.com/boppreh/aes)

SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
SRC_DIR="${SCRIPT_PATH}/src"
EXE="$SRC_DIR/ecc.py"

enc_input_file=$1
enc_output_file=$2
cipher_key=$3

# This calls the the algorithm with the specified file as input, the specified output file, and cipher key
#   $EXE encrypt "$enc_output_file" "$cipher_key" < $enc_input_file
$EXE encrypt "$enc_input_file" "$enc_output_file" "$cipher_key"
