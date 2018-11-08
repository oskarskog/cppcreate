#!/bin/bash

[[ -d ./build ]] || mkdir build

pushd build
cmake ..
popd

ln -sf ./build/compile_commands.json compile_commands.json
