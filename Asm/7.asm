.include "things.asm"
main:
    call read_dec
    call write_dec
    exit 0

read_dec: #-->a0 also use: t0 t1 t2 t3
	li t0 0
	li t1 '\n'
	li t2 0x80000000
    li t4 48
    li t5 10
_read_dec_before_loop:
    read
    li t3 '-'   
    beq a0 t3 _read_dec_negative
    li t3 0
    j _read_dec_main_loop
_read_dec_negative:
    li t3 1 #sign
_read_dec_loop:
	read
_read_dec_main_loop:
    bgeu t0 t2 _read_dec_error
	beq a0 t1 _read_dec_end
	blt a0 t4 _read_dec_error
    sub a0 a0 t4
    bge a0 t5 _read_dec_error

    slli t6 t0 1 #multiple 10
    slli t0 t0 3
    add t0 t0 t6

    add t0 t0 a0

	j _read_dec_loop
_read_dec_end:
    mv a0 t0
    beq t3 zero _read_dec_quit
    sub a0 zero a0
_read_dec_quit:
    ret
_read_dec_error:
	exit 1

write_dec: # a0-> also use t0 t1
    push ra
    li t1 0 #counter

	mv t0 a0
    li t2 0x80000000
    and t2 t2 t0
    beq t2 zero _write_dec_stack_loop
    sub t0 zero t0
    writi '-'
_write_dec_stack_loop:
	mv a0 t0
    push_2 t0 t1
    call mod10
    pop_2 t0 t1
	
    addi a0 a0 48
	push a0
    addi t1 t1 1

    mv a0 t0
    push t1
    call div10
    pop t1
    mv t0 a0

	beq zero t0 _write_dec_loop
	j _write_dec_stack_loop
_write_dec_loop:
    beq t1 zero _write_dec_end
    addi t1 t1 -1
    pop a0
    write
    j _write_dec_loop
_write_dec_end:
    pop ra
	ret

div10: #a0->a0 also use
    li t1 0x80000000
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
    li t0 0x80000000 #remove sign
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