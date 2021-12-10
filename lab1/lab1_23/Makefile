##################################################################
# To run the make, you should have the following tools available:
#
#   * rvv clang/llvm (https://github.com/isrc-cas/rvv-llvm)
#   * riscv gcc elf toolchain (https://github.com/riscv/riscv-gnu-toolchain)
#   * spike (https://github.com/riscv/riscv-isa-sim)
#   * pk (https://github.com/riscv/riscv-pk)
#
##################################################################

# Change the path for your environment.

GCC_TOOLCHAIN_DIR := {Your_Dir}/riscv-gnu-toolchain_rvv-0.9.x
SYSROOT_DIR := $(GCC_TOOLCHAIN_DIR)/riscv64-unknown-elf

CLANG := clang
SPIKE := spike
PK := pk

objects = mtmac.c mtmac.s
target = mtmac-test

$(target) : $(objects)
	$(CLANG)  --target=riscv64-unknown-elf -menable-experimental-extensions -march=rv64gcv1p0 --sysroot=$(SYSROOT_DIR) --gcc-toolchain=$(GCC_TOOLCHAIN_DIR) -o $(target) $(objects)

run :
	$(SPIKE) $(PK) -s $(target)

clean :
	rm -f $(target)
