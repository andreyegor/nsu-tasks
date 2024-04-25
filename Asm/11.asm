.include "things.asm"

.text
.globl main

main:
    lw a0 0(a1)
    write_str

    li a1 0
    call fopen
    mv s0 a0
    call fload

    li a0 ' '
    write

    mv a0 s0
    call flength
    call write_dec
    
    mv a0 s0
    closef
    exit 0