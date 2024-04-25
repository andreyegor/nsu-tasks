.include "things.asm"

.text
.globl main
main:
    lw a0 0(a1)
    li a1 0
    call fopen
    mv s0 a0
    call fload
    call countlines
    call write_dec
    mv a0 s0
    closef
    exit 0
