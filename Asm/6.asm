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
    writi '\n'
    mv a0 s0
    call mul10
    call write_dec
    exit 0

mul10:
    slli t1 a0 1 #multiple 10 TODO
    slli a0 a0 3
    add a0 a0 t1
    ret