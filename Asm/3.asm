.include "things.asm"

#main code
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
	j write
sub:
	sub s4 s1 s2
	j write
and:
	and s4 s1 s2
	j write
or: 
	or s4 s1 s2
	j write
write:
	writi '\n'
	mv a0 s4
	call count_bytes_bits
	mv s5 a0
write_loop:
	srl a0 s4 s5
	call num_to_ascii
	write
	sll a0 a0 s5
	sub s4 s4 a0
	beq zero s5 end
	addi s5 s5 -4
	j write_loop
end:
	exit 0

#functions
ascii_to_num: #a0-->a0 also use: t5
	li t5 16
	addi a0 a0 -48
	blt a0 zero _ascii_to_num_invalid_exit
	blt a0 t5 _ascii_to_num_quit
	
	addi a0 a0 -7
	blt a0 t5 _ascii_to_num_quit
	
	addi a0 a0 -32
	blt a0 zero _ascii_to_num_invalid_exit
	ret
_ascii_to_num_invalid_exit:
	exit 1
_ascii_to_num_quit:
	ret 
	

read_num: #-->a0 also use: t2 t3 t4
	li t2 0
	li t3 '\n'
_read_num_loop:
	read
	beq a0 t3 _read_num_quit
	
	mv t4 ra
	call ascii_to_num
	mv ra t4
	
	slli t2 t2 4
	add t2 t2 a0
	j _read_num_loop
_read_num_quit:
	mv a0 t2
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
	
num_to_ascii: #a0-->a0 also use: t0 t1
	mv t0 a0
	li t1 10
	bge t0 t1 _num_to_ascii_more
	addi a0 t0 48
	ret
_num_to_ascii_more:
	addi a0 t0 55
	ret
	

	
