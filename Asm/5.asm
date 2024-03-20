.include "things.asm"

#main_code
main:
    call read_num
	mv s0 a0
	call read_num
	mv s1 a0
    li s2 0x80000000
    li s3 32 
_main_loop:
    srl s2 s2 1
    addi s3 s3 -1
    beq s2 zero _main_end
    and s4 s2 s1
    beq s4 zero _main_loop
    sll s0 s0 s3
_main_end:
    exit 0


#functions
write_num: # a0-> also use t0 t1
	mv t0 a0

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
_read_num_loop:
	read
	beq a0 t1 _read_num_quit
	bge t0 t2 _read_num_error
	
	push_4 ra t0 t1 t2
	call ascii_to_num
	pop_4 ra t0 t1 t2

	slli t0 t0 4
	add t0 t0 a0
	j _read_num_loop
_read_num_quit:
	mv a0 t0
	ret
_read_num_error:
	exit 1
	
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
