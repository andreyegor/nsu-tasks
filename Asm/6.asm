.include "things.asm"
.text
.globl main

main:
    call read_dec
    mv s0 a0
    call div10
    call write_dec
    writi '\n'
    mv a0 s0
    call mod10
    call write_dec
    exit 0