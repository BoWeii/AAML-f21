    .text
    .balign 4
    .global saxpy_no_rvv
# void
# saxpy(size_t n, const float a, const float *x, float *y)
# {
#   size_t i;
#   for (i=0; i<n; i++)
#     y[i] = a * x[i] + y[i];
# }
#
# register arguments:
#     a0      n
#     fa0     a
#     a1      x
#     a2      y

# Please finish this RISC-V V extension code.
add s2,zero,zero
con1:
    bge s2, a0, exit
saxpy_no_rvv:
	flw fs0,0(a1)
	flw fs1,0(a2)
    fmul.s fs0,fa0,fs0
    fadd.s fs1,fs0,fs1
    fsw fs1,0(a2)
    addi a1,a1,4
    addi a2,a2,4
    addi s2,s2,1
	j con1
    ret
exit:
    ret
