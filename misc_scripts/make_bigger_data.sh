#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

FILE_ORIG=$SCRIPTPATH/data_to_encrypt/alice_larger.txt
OUTPUT_FILE=$SCRIPTPATH/data_to_encrypt/alice_largest.txt

touch $OUTPUT_FILE
for (( i=0; i<20; i++)); do
    cat $FILE_ORIG >> $OUTPUT_FILE
done