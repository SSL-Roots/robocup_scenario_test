#!/bin/bash
# Compile proto files for python

# Modify import path of generated python files.
# For example:
#   Before:
#     import ssl_vision_geometry_pb2 as ssl__vision__geometry__pb2
#   After:
#     from . import ssl_vision_geometry_pb2 as ssl__vision__geometry__pb2
# 
function modify_import_path () {
    python_files=$(find $1 -name "*.py")

    for file in $python_files; do
        echo "Modifying import path of $file"
        # Ignore lines starting with "from"
        sed -i '/^from/!s/import \(.*\)_pb2/from . import \1_pb2/' "$file"
    done
}

function compile () {
    echo "Compiling $1"
    protoc -I=$1 --python_out=$1 $1/*.proto
    modify_import_path $1
}

cd $(dirname $0)

compile ./proto
