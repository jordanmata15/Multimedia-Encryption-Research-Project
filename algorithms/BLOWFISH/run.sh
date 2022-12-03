#!/bin/bash

enc_input_file=$1
enc_output_file=$2
compression=$3

# This calls the the algorithm with the specified file as input, the specified output file
gpg --symmetric --batch --yes --passphrase 'ComputerScience' --compress-algo "$compression" --cipher-algo BLOWFISH -o "$enc_output_file" "$enc_input_file"
