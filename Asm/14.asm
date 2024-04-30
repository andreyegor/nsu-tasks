.include "things.asm"

.text
.globl main
main:
    li s6 'v'
    li s7 'n'
    li s8 'c'
    li s9 'i'

    beq a0 zero _main_err
    addi a0 a0 -1
    lw s0 0(a1)
    addi a1 a1 4
    li t1 '-'
    beq a0 zero _main_continue
_main_read_loop:
    lw s1 0(a1)
    addi a0 a0 -1
    addi a1 a1 4
    beq a0 zero _main_continue
    lb t0 0(s1)
    bne t0 t1 _main_continue
    lb t0 1(s1)
    set_flag t0 s6
    set_flag t0 s7
    set_flag t0 s8
    set_flag t0 s9
    j _main_read_loop
_main_continue:
    mv a0 s0
    li a1 0
    call fopen
    mv s5 a0
    call fload
    call splitlines

    li t0 -1
    bne s1 t0 _main_write
    lw s1 0(a0)
    li s4 0 #counter
_main_write:
    lw t0 0(a0)
    mv s3 t0
    addi a0 a0 4
    mv s2 a0
    li s10 0
_main_write_loop:
    lw a0 0(s2)
    mv a1 s1
    call strstr
    beq a0 zero _main_write_loop_end
    beq s8 zero _main_write_loop_just_counter
    mv a0 s4
    call write_dec
    writi':'
    writi' '
    lw a0 0(s2)
    write_str
    writi'\n'
_main_write_loop_just_counter:
    addi s10 s10 1
_main_write_loop_end:
    addi s4 s4 1
    addi s2 s2 4
    bne s4 s3 _main_write_loop
_main_after_loop:
    bne s8 zero _main_end
    mv a0 s10
    call write_dec
_main_end:
    mv a0 s5
    closef
    exit 0
_main_err:
    exit(1)