    .text
    .balign 4
    .global tensormul
tensormul:
    vsetvli t0, a0, e32, m4, ta, ma  # Set vector length based on 32-bit vectors
    vle32.v v4, (a1)       # Get first vector x
      sub a0, a0, t0         # Decrement number done
      slli t0, t0, 2         # Multiply number done by 4 bytes
      add a1, a1, t0         # Bump pointer
    vle32.v v8, (a2)       # Get second vector y
      // add a2, a2, t0         # Bump pointer
    vle32.v v0, (a3)
     .word 0xe2824057       # Instruction machine code  <<<You only have to modify this line>>>
    vse32.v v0, (a3)          # Store result z
      add a3, a3, t0         # Bump pointer
      bnez a0, tensormul     # Loop back
      ret                    # Finished
