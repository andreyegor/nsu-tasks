.include "things.asm"

.text
.globl main
main:
    lw a0 0(a1)
    li a1 0
    call fopen
    mv s0 a0
    call fload
    addi a0 a0 -1
_main_loop:
    addi a0 a0 1
    addi s1 s1 1
    li a1 '\n'
    call strchr
    bne a0 zero _main_loop
    mv a0 s1
    call write_dec
    mv a0 s0
    closef
    exit 0
