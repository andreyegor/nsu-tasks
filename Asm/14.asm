.include "things.asm"

.text
.globl main
main:
    li t0 2
    bne a0 t0 _main_err
    lw s0 0(a1)
    lw s1 4(a1)
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
_main_write_loop:
    lw a0 0(s2)
    mv a1 s1
    call strstr
    beq a0 zero _main_write_loop_end
    mv a0 s4
    call write_num
    writi':'
    writi' '
    lw a0 0(s2)
    write_str
    writi'\n'
_main_write_loop_end:
    addi s4 s4 1
    addi s2 s2 4
    bne s4 s3 _main_write_loop
_main_end:
    mv a0 s5
    closef
    exit 0
_main_err:
    exit(1)