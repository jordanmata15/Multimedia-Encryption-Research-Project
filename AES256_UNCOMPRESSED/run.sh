#!/bin/bash

enc_input_file=$1
enc_output_file=$2

# This calls the the algorithm with the specified file as input, the specified output file
gpg --symmetric --batch --yes --passphrase 'ComputerScience' --compress-algo none --cipher-algo AES256 -o "$enc_output_file" "$enc_input_file"
