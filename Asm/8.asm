.include "things.asm"

.text
.globl main
main:
    call read_dec
    mv s1 a0
    call read_dec
    mv s2 a0
    read
    mv s3 a0
    writi '\n'
    li t0 '+'
    beq s3 t0 _main_add
    li t0 '-'
	beq s3 t0 _main_sub
    li t0 '&'
	beq s3 t0 _main_and
    li t0 '|'
	beq s3 t0 _main_or
    li t0 '*'
    beq s3 t0 _main_mul
    exit 1
_main_add:
    add s0 s1 s2

    li t0 0x80000000
    xor t1 s1 s2
    and t2 t0 t1
    bne t2 zero _main_continue
    and t2 t0 s0
    beq t2 zero _main_positive_overflow_check
    j _main_negative_overflow_check
_main_sub:
    sub s0 s1 s2 

    li t0 0x80000000
    xor t1 t0 s2
    xor t2 s1 t1
    and t3 t0 t2
    bne t3 zero _main_continue
    and t3 t0 s0
    beq t3 zero _main_positive_overflow_check
    j _main_negative_overflow_check

    j _main_continue
_main_and:
    and s0 s1 s2
    j _main_continue
_main_or:
    or s0 s1 s2
    j _main_continue
_main_mul:
    mv a0 s1
    mv a1 s2
    push ra
    call mul
    pop ra
    mv s0 a0
    j _main_continue
_main_positive_overflow_check:
    blt s0 zero _main_error
    j _main_continue
_main_negative_overflow_check:
    bgt a0 zero _main_error
    j _main_continue
_main_continue:
    mv a0 s0
    call write_dec
    exit 0
_main_error:
    exit 1
