.text
.macro syscall %n
	li a7, %n
	ecall
.end_macro

.macro read
	syscall 12
.end_macro

.macro write
	syscall 11
.end_macro 

.macro writi %c
	li a0 %c
	write
.end_macro  

.macro exit %code
	li a0 %code
	syscall 93
.end_macro

.macro swap %r1, %r2
	xor %r1, %r1, %r2
	xor %r2, %r2, %r1
	xor %r1, %r1, %r2
.end_macro

.macro push %r1
	addi sp, sp, -4
	sw %r1, 0(sp)
.end_macro

.macro pop %r1
	lw %r1, 0(sp)
	addi sp, sp, 4
.end_macro

.macro push_2 %r1 %r2
	addi sp, sp, -8
	sw %r1, 0(sp)
	sw %r2, 4(sp)
.end_macro

.macro pop_2 %r1 %r2
	lw %r1, 0(sp)
	lw %r2, 4(sp)
	addi sp, sp, 8
.end_macro

.macro push_3 %r1 %r2 %r3
	addi sp, sp, -12
	sw %r1, 0(sp)
	sw %r2, 4(sp)
	sw %r3, 8(sp)
.end_macro

.macro pop_3 %r1 %r2 %r3
	lw %r1, 0(sp)
	lw %r2, 4(sp)
	lw %r3, 8(sp)
	addi sp, sp, 12
.end_macro

.macro push_4 %r1 %r2 %r3 %r4
	addi sp, sp, -16
	sw %r1, 0(sp)
	sw %r2, 4(sp)
	sw %r3, 8(sp)
	sw %r4, 12(sp)
.end_macro

.macro pop_4 %r1 %r2 %r3 %r4
	lw %r1, 0(sp)
	lw %r2, 4(sp)
	lw %r3, 8(sp)
	lw %r4, 12(sp)
	addi sp, sp, 16
.end_macro

.macro push_5 %r1 %r2 %r3 %r4 %r5
	addi sp, sp, -16
	sw %r1, 0(sp)
	sw %r2, 4(sp)
	sw %r3, 8(sp)
	sw %r4, 12(sp)
	sw %r5, 16(sp)
.end_macro

.macro pop_5 %r1 %r2 %r3 %r4 %r5
	lw %r1, 0(sp)
	lw %r2, 4(sp)
	lw %r3, 8(sp)
	lw %r4, 12(sp)
	lw %r5 16(sp)
	addi sp, sp, 20
.end_macro

#functions
read_dec: #-->a0 also use: t0 t1 t3 t4
	li t0 0
	li t1 '\n'
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
    blt t0 zero _read_dec_error
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
    beq t1 zero _div_10_continue
	sub a0 zero a0
_div_10_continue:
    li t0 9
    ble a0 t0 _div10_zero

    srli t0 a0 2

    push_3 ra t0 t1
    srli a0 a0 1
    call div10
    pop_3 ra t0 t1

    sub a0 t0 a0
    srli a0 a0 1
	beq t1 zero _div_10_ret
    sub a0 zero a0
_div_10_ret:
    ret
_div10_zero:
    li a0 0
    ret

mod10:
    li t0 0x80000000 #remove sign
    and t0 t0 a0
    beq t0 zero _mod_10_continue
	sub a0 zero a0
_mod_10_continue:
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
