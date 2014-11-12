#!/bin/bash -e

BUILD_FILE=${BUILD_FILE-atrocity_watch.json}
VARIABLE_FILE=${VARIABLE_FILE-variables.json}

if [ ! -f $VARIABLE_FILE ]; then
    echo "Must have $VARIABLE_FILE with appropriate variables defined"
    echo "You can start with variables_example.json"
    exit 1
fi

echo "Validating config ... "
packer validate -var-file=$VARIABLE_FILE $BUILD_FILE

echo "Build options: $*"

packer build \
    -var-file=$VARIABLE_FILE \
    $* \
    $BUILD_FILE 

