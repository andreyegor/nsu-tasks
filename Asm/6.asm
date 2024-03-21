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
    call write_num
    exit 0

div10: #a0->a0 also use
    li t1 0x10000000
    and t1 t1 a0 #sign
    xor a0 a0 t1

    li t0 9
    ble a0 t0 _div10_zero

    srli t0 a0 2

    push_3 ra t0 t1
    srli a0 a0 1
    call div10
    pop_3 ra t0 t1

    sub a0 t0 a0
    srli a0 a0 1
    add a0 a0 t1
    ret
_div10_zero:
    li a0 0
    ret

mod10:
    li t0 0x10000000 #remove sign
    or a0 a0 t0
    xor a0 a0 t0

    mv t0 a0
    push_2 ra t0
    call div10
    pop_2 ra t0

    slli t1 a0 1 #multiple 10
    slli a0 a0 3
    add a0 a0 t1

    sub a0 t0 a0
    ret

write_num: # a0-> also use t0 t1
	mv t0 a0
    li t1 0x10000000
    and t1 t1 t0
    beq t1 zero _write_num_count
    writi '-'
    xor t0 t0 t1
    mv a0 t0
_write_num_count:
    push_3 ra t0
	call count_bytes_bits
    pop_3 ra t0

	mv t1 a0
_write_num_loop:
	srl a0 t0 t1
	
	push_3 ra t0 t1
	call num_to_ascii
	pop_3 ra t0 t1

	write
	sll a0 a0 t1
	sub t0 t0 a0
	beq zero t1 _write_num_end
	addi t1 t1 -4
	j _write_num_loop
_write_num_end:
	ret

ascii_to_num: #a0-->a0 also use: t0
	li t0 16
	addi a0 a0 -48
	blt a0 zero _ascii_to_num_invalid_exit
	blt a0 t0 _ascii_to_num_quit
	
	addi a0 a0 -7
	blt a0 t0 _ascii_to_num_quit
	
	addi a0 a0 -32
	blt a0 zero _ascii_to_num_invalid_exit
	ret
_ascii_to_num_invalid_exit:
	exit 1
_ascii_to_num_quit:
	ret 
	
read_num: #-->a0 also use: t0 t1 t2
	li t0 0
	li t1 '\n'
	li t2 0x10000000
_read_num_before_loop:
    read
    li t3 '-'
    beq a0 t3 _read_num_negative
    li t3 0
    j _read_num_main_loop
_read_num_loop:
	read
_read_num_main_loop:
    bgeu t0 t2 _read_num_error
	beq a0 t1 _read_num_quit
	
	push_5 ra t0 t1 t2 t3
	call ascii_to_num
	pop_5 ra t0 t1 t2 t3

	slli t0 t0 4
	add t0 t0 a0
	j _read_num_loop
_read_num_quit:
    add a0 t0 t3
	ret
_read_num_error:
	exit 1
_read_num_negative:
    li t3 0x10000000 #sign
    j _read_num_loop
	
count_bytes_bits: #a0-->a0, also use t0
	mv t0 a0
	li a0 0
	beq zero t0 _count_bytes_bits_quit
_count_bytes_bits_loop:
	srli t0 t0 4
	beq zero t0 _count_bytes_bits_quit
	addi a0 a0 4
	j _count_bytes_bits_loop
_count_bytes_bits_quit:
	ret
	
num_to_ascii: #a0-->a0 also use: t0 t1
	mv t0 a0
	li t1 10
	bge t0 t1 _num_to_ascii_more
	addi a0 t0 48
	ret
_num_to_ascii_more:
	addi a0 t0 55
	ret
