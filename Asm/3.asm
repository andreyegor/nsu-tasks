.include "things.asm"


main:
	li s8 '+'
	li s9 '-'
	li s10 '&'
	li s11 '|'
	
	call read_num
	mv s1 a1
	call read_num
	mv s2 a1
	read
	mv s3 a0
	
	beq s3 s8 add
	beq s3 s9 sub
	beq s3 s10 and
	beq s3 s11 or
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
	mv a1 s4
	call count_bytes_bits
	mv s5 a0
write_loop:
	srl a1 s4 s5
	call num_to_ascii
	write
	sll a1 a1 s5
	sub s4 s4 a1
	beq zero s5 end
	addi s5 s5 -4
	j write_loop
	
end:
	exit
	
quit:#nothing
	ret
	
to_num: #a0-->a0 also write:t1
	li t1 16
	addi a0 a0 -48
	blt a0 t1 quit
	addi a0 a0 -7
	ret

read_num: #-->a1 also write: a0 t0 t6
	li a1 0
	li t0 '\n'
_read_num_loop:
	read
	beq a0 t0 quit
	
	mv t6 ra
	call to_num
	mv ra t6
	
	slli a1 a1 4
	add a1 a1 a0
	j _read_num_loop
	
count_bytes_bits: #a1-->a0, also write: a1
	li a0 0
	beq zero a1 quit
count_bytes_bits_loop:
	srli a1 a1 4
	beq zero a1 quit
	addi a0 a0 4
	j count_bytes_bits_loop
	
num_to_ascii: #a1-->a0 also write: t0
	li t0 10
	bge a1 t0 _num_to_ascii_more
	addi a0 a1 48
	ret
_num_to_ascii_more:
	addi a0 a1 55
	ret
	

	