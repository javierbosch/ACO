#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <test file name>"
    exit 1
fi

sbatch --partition=Teach-Standard --mincpus=4 -D /home/s1915183/Java-ACO-clean/ACO run.sh $1