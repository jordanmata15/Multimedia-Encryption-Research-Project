#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PACKAGE_DIR="${SCRIPTPATH}/.."
DATA_DIR="${PACKAGE_DIR}/Data_Sets"
ENCRYPTED_DATA_DIR="${PACKAGE_DIR}/Encrypted_Data"

SRC_DIR="${SCRIPTPATH}/src"
EXE="$SRC_DIR/aes.py"

CIPHER_KEY="This is a cipher key"

# encrypt each file in the DATA_DIR. 
# Write encrypted file in ENCRYPTED_DATA_DIR with extension enc
for data_filename in $DATA_DIR/*; do
    filename_without_ext=$(basename $data_filename .txt)
    encrypted_filepath=$ENCRYPTED_DATA_DIR/$filename_without_ext.enc
    
    # This part of the line lets us avoid context switches to get more accurate times
    #   sudo chrt -f 99 /usr/bin/time --verbose
    # The rest is calls the  the algorithm with the specified file as input
    sudo chrt -f 99 /usr/bin/time --verbose $EXE encrypt "$encrypted_filepath" "$CIPHER_KEY" < $data_filename
    echo
done

# decrypt all files in the ENCRYPTED_DATA_DIR folder
for encrypted_filename in $ENCRYPTED_DATA_DIR/*; do
    filename_without_ext=$(basename $encrypted_filename .enc)
    encrypted_filepath=$ENCRYPTED_DATA_DIR/$filename_without_ext.enc
    
    # This part of the line lets us avoid context switches to get more accurate times
    #   sudo chrt -f 99 /usr/bin/time --verbose
    # The rest is calls the  the algorithm with the specified file as input
    sudo chrt -f 99 /usr/bin/time --verbose $EXE decrypt "/dev/null" "$CIPHER_KEY" < $encrypted_filepath
    echo
done