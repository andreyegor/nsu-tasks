.include "things.asm"
.text
.globl main
main:
	li s8 '+'
	li s9 '-'
	li s10 '&'
	li s11 '|'
	
	call read_num
	mv s1 a0
	call read_num
	mv s2 a0
	read
	mv s3 a0

	beq s3 s8 add
	beq s3 s9 sub
	beq s3 s10 and
	beq s3 s11 or
	exit 1
add:
	add s4 s1 s2
	j continue
sub:
	sub s4 s1 s2
	j continue
and:
	and s4 s1 s2
	j continue
or: 
	or s4 s1 s2
	j continue
continue:
	writi '\n'
	mv a0 s4
	call write_num
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
	
num_to_ascii: #a0-->a0 also use: t0 t1
	mv t0 a0
	li t1 10
	bge t0 t1 _num_to_ascii_more
	addi a0 t0 48
	ret
_num_to_ascii_more:
	addi a0 t0 55
	ret
	

	
