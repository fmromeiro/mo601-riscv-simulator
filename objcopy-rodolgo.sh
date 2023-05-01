#!/bin/bash

mkdir -p 'test/build/bin'

for f in Programas\ RISC-V\ compilados/*.riscv; do
    filename=$(basename -- "$f")
    filename="${filename%.*}"
    riscv64-linux-gnu-objcopy -j .text -j .rodata -O binary "$f" "test/build/bin/${filename}.bin"
done