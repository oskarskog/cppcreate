#!/bin/bash

function build {
    pushd ./build
    make -j4
    popd
}

if [ -d ./build ]; then
    echo exists
    build
else
    bash ./cmake.sh
    build
fi
