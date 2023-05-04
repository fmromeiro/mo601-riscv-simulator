#!/bin/bash

mkdir -p 'test/build/bin'

for f in "$1"/*.riscv; do
    filename=$(basename -- "$f")
    filename="${filename%.*}"
    riscv64-linux-gnu-objcopy -O binary "$f" "test/build/bin/${filename}.bin"
done