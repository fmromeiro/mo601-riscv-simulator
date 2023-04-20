FROM ghcr.io/guibrandt/riscv-gnu-toolchain:rv32im-ilp32

RUN apt-get update && apt-get install -y make && apt-get --reinstall install -y libmpc3

ENV LD_LIBRARY_PATH /usr/local/lib

RUN ldconfig

WORKDIR /mnt/test

ENTRYPOINT [ "make", "build" ]