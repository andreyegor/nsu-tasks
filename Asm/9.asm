.include "things.asm"

.text
.globl main

main:
    li a0 42
    li a1 7
    li s0 6
    call udiv
    bne a0 s0 _main_err

    li a0 0xffffffff
    li a1 2
    li s0 0x7fffffff
    call udiv
    bne a0 s0 _main_err

    li a0 -42
    li a1 7
    li s0 -6
    call sdiv
    bne a0 s0 _main_err

    li a0 -42
    li a1 -7
    li s0 6
    call sdiv
    bne a0 s0 _main_err

    li a0 -7
    li a1 42
    li s0 0
    call sdiv
    bne a0 s0 _main_err

    call read_dec
	mv s0 a0
	call read_dec
	mv a1 a0
    mv a0 s0
    call sdiv
    call write_dec
    exit 0
_main_err:
    exit 1


udiv:
    beq a1 zero _udiv_err
    mv t0 a0
    mv t1 a1
    li a0 1
    beq t0 t1 _udiv_end
    
    mv a0 t1
    push_3 ra t0 t1
    call count_bytes
    pop_3 ra t0 t1
    mv t3 a0

    mv a0 t0
    push_4 ra t0 t1 t3
    call count_bytes
    pop_4 ra t0 t1 t3
    
    sub t2 a0 t3
    li a0 0
    blt t2 zero _udiv_end
    sll t2 t1 t2

    srli t1 t1 1
_udiv_loop:
    slli a0 a0 1
    bltu t0 t2 _udiv_shift
    addi a0 a0 1
    sub t0 t0 t2
_udiv_shift:
    srli t2 t2 1
    bne t2 t1 _udiv_loop
_udiv_end:
    ret
_udiv_err:
    exit 1


sdiv:
    li t2 0xf0000000 #sign
    and t0 a0 t2
    and t1 a1 t2
    xor t0 t0 t1#sign

    bge a0 zero _sdiv_second_sign
    sub a0 zero a0 
_sdiv_second_sign:
    bge a1 zero _sdiv_continue
    sub a1 zero a1 
_sdiv_continue:
    push_2 ra t0
    call udiv
    pop_2 ra t0
    beq t0 zero _sdiv_quit
    sub a0 zero a0
_sdiv_quit:
    ret