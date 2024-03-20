.include "things.asm"

#main_code
main:
    call read_num
	mv s0 a0#first number
	call read_num
	mv s1 a0#second number
    li s2 0x80000000#iterator
    li s3 31#iterator too
    li s4 0xf0000000#out of range
    li a0 0 #result
    
    li s5 0
    and s5 s0 s4
    and t0 s1 s4
    xor s5 s5 t0 #sign
    
    or s0 s0 s4
    or s1 s1 s4
    xor s0 s0 s4
    xor s1 s1 s4
_main_loop:
    srli s2 s2 1
    addi s3 s3 -1
    beq s2 zero _main_end 

    and t0 s2 s1
    beq t0 zero _main_loop

    sll t1 s0 s3

    srl t2 t1 s3
    bne s0 t2 _main_err
    add a0 a0 t1

    and t2 a0 s4
    bne t2 zero _main_err

    j _main_loop
_main_end:
    add a0 a0 s5
    call write_num
    exit 0
_main_err:
    exit 1


#functions
write_num: # a0-> also use t0 t1
	mv t0 a0
    li t1 0x10000000
    and t1 t1 t0
    beq t1 zero _write_num_count
    writi '-'
    xor t0 t0 t1
_write_num_count:
	push ra
	push t0
	call count_bytes_bits
	pop t0
	pop ra

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
