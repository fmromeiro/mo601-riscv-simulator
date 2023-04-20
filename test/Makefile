CC		= "riscv64-unknown-elf-gcc"
OBJCOPY	= "riscv64-unknown-elf-objcopy"

BUILD_DIR 	= build
ELF_DIR 	= $(BUILD_DIR)/elf
BIN_DIR 	= $(BUILD_DIR)/bin

ELF_SUFFIX = .riscv
BIN_SUFFIX = .bin

ECHO 	= /bin/echo

CFLAGS 		= -g -march=rv32im -std=gnu99 -mabi=ilp32
LINK_OPTS 	= -T riscv/test.ld -nostartfiles

$(ELF_DIR):
	mkdir -p $(ELF_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# Compile programs
$(ELF_DIR)/%$(ELF_SUFFIX): %.c
	$(CC) $(CFLAGS) riscv/crt.s $< -o $@ $(LIB_DIR) $(LIBS) $(CFLAGS) $(LINK_OPTS)

$(BIN_DIR)/%$(BIN_SUFFIX): $(ELF_DIR)/%$(ELF_SUFFIX)
	$(OBJCOPY) -O binary $< $@

build: $(ELF_DIR) $(BIN_DIR) $(patsubst %.c,$(BIN_DIR)/%$(BIN_SUFFIX),$(wildcard *.c)) $(patsubst %.c,$(ELF_DIR)/%$(ELF_SUFFIX),$(wildcard *.c))

run: build
	# TODO

clean: 
	rm -f $(TESTS)
	rm -f *~
	rm -f *.cmd
	rm -f *.out
	rm -rf $(BUILD_DIR)

.PHONY: build clean

.PRECIOUS: $(ELF_DIR)/%$(ELF_SUFFIX)