#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <test file name>"
    exit 1
fi

cd bin
java Main $1