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

