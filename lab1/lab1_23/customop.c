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