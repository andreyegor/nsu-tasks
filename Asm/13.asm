.include "things.asm"

.text
.globl main
main:
    beq a0 zero _main_err
    lw s0 0(a1)
    li t0 1
    li s1 -1
    beq a0 t0 _main_continue
    lw a0 4(a1)
    call dec_to_int
    mv s1 a0
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
_main_write:
    beq s1 zero _main_end
    lw s3 0(a0)
    mv s4 s3
    sub s3 s3 s1
    blt s3 zero _main_err
    bgt s3 s4 _main_err
    addi a0 a0 4

    add s2 a0 s3
    add s2 s2 s3
    add s2 s2 s3
    add s2 s2 s3
_main_write_loop:
    mv a0 s3
    call write_num
    writi':'
    writi' '
    lw a0 0(s2)
    write_str
    writi'\n'
    addi s2 s2 4
    addi s3 s3 1
    bne s3 s4 _main_write_loop
_main_end:
    mv a0 s5
    closef
    exit 0
_main_err:
    exit(1)