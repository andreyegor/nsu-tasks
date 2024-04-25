.include "things.asm"
.text
.globl main
main:
    call read_bcd
    mv s0 a0
    call read_bcd
    mv s1 a0
    read
    mv s2 a0
    writi '\n'

    li s3 '+'
    beq s2 s3 _main_add
    li s3 '-'
    beq s2 s3 _main_sub
    exit 1
_main_add:
    mv a0 s0
    mv a1 s1
    call add
    j _main_continue
_main_sub:
    mv a0 s0
    mv a1 s1
    call sub
    j _main_continue
_main_continue:
    call write_bcd
    exit 0


#functions
#add is unsigned
add:#a0 a1 --> a0 also use: t0 t1 t2 t3 t4 t5 t6
    srli t0 a0 28
    srli t1 a1 28
    xor t0 t0 t1
    bne t0 zero _add_sub

    li t0 0 #result
    beq t1 zero _add_before_loop 
    li t0 0x10000000
_add_before_loop:
    swap t0 a0 #left and result
    mv t1 a1 #right
    li t2 0 #carry
    li t3 28 #iterator
    li t6 10 #notation

_add_loop:
    beq t3 zero _add_end

    sll t4 t0 t3 #left sign
    srl t4 t4 t3
    sub t0 t0 t4

    sll t5 t1 t3 #right sign
    srl t5 t5 t3
    sub t1 t1 t5

    add t4 t4 t5
    add t4 t4 t2

    add a0 a0 t4
    
    addi t3 t3 -4
    bge t4 t6 _add_carry
    li t2 0
    slli t6 t6 4
    j _add_loop
_add_carry:
    li t2 0x10000000
    srl t2 t2 t3
    sub a0 a0 t6
    slli t6 t6 4
    beq t6 zero _add_err
    j _add_loop
_add_end:
    # xor a0 a0 t2 # for minus sign
    ret
_add_err:
    exit 1
_add_sub:
    push ra
    li t0 0x10000000
    xor a1 a1 t0
    call sub #j sub
    pop ra
    ret

#also unsigned
sub:#a0 a1 --> a0 also use: t0 t1 t2 t3 t4 t5 t6
    srli t0 a0 28
    srli t1 a1 28
    xor t0 t0 t1
    bne t0 zero _sub_add #this is add
    mv t1 a1
    push_2 ra t1
    call sort_2
    pop_2 ra t1
    bne a0 t1 _sub_negative
    mv t0 a1
    mv t1 a0
    li a0 0 #result
    j _sub_before_loop
_sub_negative:
    mv t0 a1
    mv t1 a0
    li a0 0x10000000 #set negative sign
_sub_before_loop:
    li t2 0 #carry
    li t3 28 #iterator
    li t6 10 #notation
_sub_loop:
    beq t3 zero _sub_end

    sll t4 t0 t3 #left sign
    srl t4 t4 t3
    sub t0 t0 t4

    sll t5 t1 t3 #right sign
    srl t5 t5 t3
    sub t1 t1 t5

    add t5 t5 t2

    addi t3 t3 -4
    blt t4 t5 _sub_carry

    sub t4 t4 t5
    add a0 a0 t4

    li t2 0
    slli t6 t6 4
    j _sub_loop
_sub_carry:
    add t4 t4 t6
    sub t4 t4 t5
    add a0 a0 t4

    li t2 0x10000000
    srl t2 t2 t3
    slli t6 t6 4
    j _sub_loop
_sub_end:
    xor a0 a0 t0 # for minus sign
    ret
_sub_add:
    li t0 0x10000000
    xor a1 a1 t0
    push ra
    call add #j add
    pop ra
    ret

sort_2:#a0 a1-->a0 a1 also use: nothing
    blt a0 a1 _sort_2_quit
    swap a0 a1
_sort_2_quit:
    ret

read_bcd: #-->a0 also use: t0 t1 t2 t3 t4 t5
	li t0 0
	li t1 7
	li t2 '\n'
    li t3 '-'
    li t4 48
    li t5 58
_read_bcd_loop:
    beq t1 zero _read_bcd_error

	read
	beq a0 t2 _read_bcd_end
	beq a0 t3 _read_bcd_negative
    blt a0 t4 _read_bcd_error
    bge a0 t5 _read_bcd_error
	addi a0 a0 -48

	slli t0 t0 4
	add t0 t0 a0
    addi t1 t1 -1
	j _read_bcd_loop
_read_bcd_negative:
    bne t0 zero _read_bcd_error
    beq t3 zero _read_bcd_error
    li t3 0
    j _read_bcd_loop
_read_bcd_end:
    bne t3 zero _read_bcd_quit
    li t1 0x10000000
    add t0 t0 t1
_read_bcd_quit:
    mv a0 t0
	ret
_read_bcd_error:
	exit 1

write_bcd: # a0-> also use t0 t1 t2 t3
    mv t0 a0
    li t2 0x10000000
    and t3 t0 t2
    beq t3 zero _write_bcd_count
    sub t0 t0 t2
    beq t0 zero _write_zero
    writi '-'
_write_bcd_count:
    mv a0 t0
	push_2 ra t0
	call count_bytes_bits
	pop_2 ra t0
	mv t1 a0
_write_bcd_loop:
	srl a0 t0 t1

    addi a0 a0 48
	write
    addi a0 a0 -48

	sll a0 a0 t1
	sub t0 t0 a0
	beq zero t1 _write_bcd_end
	addi t1 t1 -4
	j _write_bcd_loop
_write_zero:
    writi '0'
_write_bcd_end:
	ret