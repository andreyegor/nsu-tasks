.include "things.asm"
.text
.globl main
main:
	li t2 '\n'
	read
	beq a0 t2 quit
	mv t0 a0
	writi '\n'
	mv a0 t0
	write
	addi t0 a0 1
	writi '\n'
	mv a0 t0
	write
	writi'\n'
	j main
	

quit:
	exit 0
