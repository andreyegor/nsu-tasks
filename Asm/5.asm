.include "things.asm"

.text
.globl main
main:
    call read_dec
	mv s0 a0#first number
	call read_dec
	mv s1 a0#second number
    li s2 0x80000000#iterator
    li s3 31#iterator too
    li s4 0xf0000000#out of range
    li a0 0 #result

    li s5 0
    and t0 s0 s4
    and t1 s1 s4
    xor s5 t0 t1 #sign

	beq t0 zero _main_second_sign
	sub s0 zero s0
_main_second_sign:
	beq t1 zero _main_loop
	sub s1 zero s1

_main_loop:
    srli s2 s2 1
    addi s3 s3 -1
    beq s2 zero _main_continue 


    and t0 s2 s1
    beq t0 zero _main_loop

    sll t1 s0 s3

    srl t2 t1 s3
    bne s0 t2 _main_err
    add a0 a0 t1

    and t2 a0 s4
    bne t2 zero _main_err

    j _main_loop
_main_continue:
	beq s5 zero _main_end
	sub a0 zero a0
_main_end:
	call write_dec
    exit 0
_main_err:
    exit 1