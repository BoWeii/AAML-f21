# LAB 1 Hints
###

## LAB 1-1
* Install them at a same directory.
* For example: `/home/$(USER)/RISCV/riscv-gnu-toolchain_rvv-0.9.x`
![image](https://github.com/BoWeii/AAML-f21/blob/master/lab1/menu.png)
### 0. Set environment variable
run`vim ~/.bashrc` in terminal
add these in the .bashrc file

```
export RISCV={RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x
export PATH=$PATH:$RISCV/bin
```
run`source ~/.bashrc` in terminal
### 1. riscv-gnu-toolchain
#### 1. Go to RISCV root directory and clone specific branch
    sudo apt-get install autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev
    git clone https://github.com/riscv/riscv-gnu-toolchain.git --branch rvv-0.9.x --single-branch --depth 1 riscv-gnu-toolchain_rvv-0.9.x
    cd riscv-gnu-toolchain_rvv-0.9.x/
    git submodule update --init --recursive --depth 1 riscv-binutils riscv-gcc riscv-glibc riscv-dejagnu riscv-newlib riscv-gdb
#### 2. Build and install
    ./configure --prefix=$RISCV --with-arch=rv64gcv --enable-multilib
    make -j8
**Note: Remember to revise your $RISCV path !!!** (/home/.../riscv-gnu-toolchain_rvv-0.9.x/)
You can use make -jx or -j to speedup.


### 2. riscv-isa-sim (Spike)
#### 1. Go to RISCV root directory and clone specific branch
    git clone https://github.com/riscv/riscv-isa-sim
    cd riscv-isa-sim/

#### 2. Build and install

    mkdir build && cd build
    sudo apt-get install device-tree-compiler
    ../configure --prefix=$RISCV --with-isa=rv64gcv
    make -j8
    make install
### 3. riscv-pk
#### 1. Build and install
    git clone https://github.com/riscv/riscv-pk
    cd riscv-pk/
    mkdir build && cd build
    ../configure --prefix=$RISCV --host=riscv64-unknown-elf --with-arch=rv64gcv 
    make -j8
    make install
    
    
run `vim ~/.bashrc` in terminal
add these in the .bashrc file
`export PATH=$PATH:{RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x/riscv64-unknown-elf/bin/`
run `source ~/.bashrc` in terminal
    
### 4. llvm/clang
#### 1. Build and install
    git clone https://github.com/plctlab/llvm-project
    cd llvm-project
    mkdir build && cd build
    
    cmake -G "Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="{RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x" \
    -DLLVM_TARGETS_TO_BUILD="RISCV" \
    -DLLVM_ENABLE_PROJECTS="clang;libcxx;libcxxabi" \
    -DLLVM_DEFAULT_TARGET_TRIPLE="riscv64-unknown-linux-gnu" \
    ../llvm
    
    cmake --build . --target install -j8
      
Note: Replace {RISCV_ROOT_DIR} with your own directory
### 5. Test benchmark

#### Compile by clang (Recommand, RISCV V extension 1.0)
    {RISCV_ROOT_DIR}/llvm-project/build/bin/clang  --target=riscv64-unknown-elf -menable-experimental-extensions -march=rv64gcv1p0 --sysroot={RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x/riscv64-unknown-elf --gcc-toolchain={RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x -o filename filename.c filename.s
clang is in `llvm-project/build/bin/`
You can use readelf or objdump to read the code file

#### Compile by toolchain(Don't use this to compile V extension)
If you use this to compile RVV code, you may encounter some problems because of the rvv version. You will get rvv 0.9 and it doesn't support some of the instuctions you found in RVV-spec or other websites.

To binary:
    `riscv64-unknown-elf-gcc -o filename filename.c filename.s`
To assembly:
    `riscv64-unknown-elf-gcc -o hello.s -S hello.c`
#### Simulation
    spike pk filename
#### Hint: You can use `spike -d pk filename` for debug, and print the register value for report writing; and use `spike pk -s filename` to count the number of instruction.

## ISA Extend Example

### Enable Spike to run custom instruction example
####  1. Open riscv-opcodes/opcodes-? 
#### (**here we took opcodes-rv32i for example, but you should try to use opcodes-rvv** for extending your vector instuction) 
#### You can find riscv-opcodes on [github](https://github.com/riscv/riscv-opcodes)
    
    sra      rd rs1 rs2 31..25=32 14..12=5 6..2=0x0C 1..0=3
    or       rd rs1 rs2 31..25=0  14..12=6 6..2=0x0C 1..0=3
    and      rd rs1 rs2 31..25=0  14..12=7 6..2=0x0C 1..0=3

    customop rd rs1 rs2 31..25=1  14..12=0 6..2=0x1A 1..0=3  <---- add this line and make sure the opcode, function 
                                                                   code are not used by other instructions.

    addiw    rd rs1 imm12            14..12=0 6..2=0x06 1..0=3
    slliw    rd rs1 31..25=0  shamtw 14..12=1 6..2=0x06 1..0=3
    srliw    rd rs1 31..25=0  shamtw 14..12=5 6..2=0x06 1..0=3
    sraiw    rd rs1 31..25=32 shamtw 14..12=5 6..2=0x06 1..0=3
    
Note: new instruction should be added to different file according to instructions format.
    
#### 2. Run 
    cat opcodes-* | ./parse_opcodes -c > ~/temp.h
    
#### 3. Open "~/temp.h" file and copy the follow two lines
    #define MATCH_CUSTOMOP 0x200006b
    #define MASK_CUSTOMOP 0xfe00707f
    
#### 4. Paste it on "riscv-isa-sim/riscv/encoding.h" and add
    #define MATCH_CUSTOMOP 0x200006b
    #define MASK_CUSTOMOP 0xfe00707f
    ...
    DECLARE_INSN(customop, MATCH_CUSTOMOP, MASK_CUSTOMOP)
    
#### 5. Define operation in "riscv-isa-sim/riscv/insns/customop.h"
    WRITE_RD(sext_xlen(RS1 % RS2));
    
    
#### 6. Revise "riscv-isa-sim/riscv/riscv.mk.in"
    riscv_insn_ext_i = \
    ...
    customop \
    ...
Note: we added in riscv_insn_ext_i due to the instruction format.

#### 7. Rebuild Spike
in riscv-isa-sim/build:
```
make clean
make -j8
make install
```
#### 8. Test program 
#### customop.c test example
```c =
    // Just for reference
    // customop.c
    #include <stdio.h>
    // Needed to verify results.
    int cusop_c(int a, int b, int c) {
        a = b % c; 
        return a;
    }
    // Should not be inlined, because we expect arguments
    // in particular registers.
    __attribute__((noinline))
    int cusop_asm(int a, int b, int c) {
        asm __volatile__ (".word 0x02C5856B\n");
        return a;
    }
    int main(int argc, char** argv) {
        int a = 2, b = 3, c = 4;
        printf("%d =?= %d\n", cusop_c(a, b, c), cusop_asm(a, b, c));
    }
```
#### 9. Compilation
    {RISCV_ROOT_DIR}/llvm-project/build/bin/clang  --target=riscv64-unknown-elf -menable-experimental-extensions -march=rv64gcv1p0 --sysroot={RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x/riscv64-unknown-elf --gcc-toolchain={RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x -o filename filename.c
    (or riscv64-unknown-elf-gcc customop.c -march=rv64gcv -o customop_test)
    spike pk customop_test

## Lab 1-2&1-3
### Hints:
#### **It took opcodes-rv32i for example, but you should use opcodes-rvv** for extending vector instuction.
#### You can find riscv-opcodes on [github](https://github.com/riscv/riscv-opcodes)
####  You may have to modify the `riscv-isa-sim/riscv/decode.h` file and others which are mention above if needed.

Compile and test ISA:

    {RISCV_ROOT_DIR}/llvm-project/build/bin/clang  --target=riscv64-unknown-elf -menable-experimental-extensions -march=rv64gcv1p0 --sysroot={RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x/riscv64-unknown-elf --gcc-toolchain={RISCV_ROOT_DIR}/riscv-gnu-toolchain_rvv-0.9.x -o mtmtp mtmtp.c mtmtp.s
    spike --isa=rv64gcv  ../riscv-gnu-toolchain_rvv-0.9.x/riscv64-unknown-elf/bin/pk mtmtp


##  Spike Debugger Usage (spike -d)
![image](https://github.com/BoWeii/AAML-f21/blob/master/lab1/spike.png)
