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
    mv s2 a0
    call fload
    call splitlines

    li t0 -1
    bne s1 t0 _main_write
    lw s1 0(a0)
_main_write:
    beq s1 zero _main_end
    lw t0 0(a0)
    sub t0 t0 s1
    ble t0 zero _main_err
    addi a0 a0 4

    add a0 a0 t0
    add a0 a0 t0
    add a0 a0 t0
    add a0 a0 t0
    lw a0 0(a0)
    write_str
_main_end:
    mv a0 s2
    closef
    exit 0
_main_err:
    exit(1)