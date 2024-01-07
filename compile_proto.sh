#!/bin/bash
# Compile proto files for python

function compile () {
    protoc -I=$1 --python_out=$1 $1/*.proto
}

cd $(dirname $0)

compile ./proto/grsim
compile ./proto/referee
compile ./proto/vision
