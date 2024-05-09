.include "things.asm"

.data
alphabet: .asciz "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-1234567890"
.text

.globl main
main:
    li s6 'c'
    li s7 'l'
    li s8 'L'
    li s9 'w'

    li t0 2 
    bne a0 t0 _main_err
    lw s0 0(a1)
    li t1 '-'
    lw t2 4(a1)
    lb t0 0(t2)
    bne t0 t1 _main_err
    lb t0 1(t2)

    set_flag t0 s6
    set_flag t0 s7
    set_flag t0 s8
    set_flag t0 s9

    mv a0 s0
    li a1 0
    call fopen
    mv s5 a0
    call fload
    mv s0 a0

    la s3 alphabet
    li s4 0 #counter

    beq s6 zero _main_chars
    beq s7 zero _main_lines
    beq s8 zero _main_max_length
    beq s9 zero _main_words
    j _main_err
_main_words:
    lb t0 0(s0)
    beq t0 zero _main_end
    mv a0 s0
    mv a1 s3
    call strcspn
    add s0 s0 a0
    mv a0 s0
    mv a1 s3
    call strspn
    beq a0 zero _main_end
    addi s4 s4 1
    add s0 s0 a0
    j _main_words
_main_max_length:
    li s2 0 #local_counter
    mv a0 s0
    call splitlines
    lw s1 0(a0) #max lines
    mv s0 a0
    li t0 0 #lines counter
_main_max_length_mx:
    blt s2 s4 _main_max_length_before_loop
    mv s4 s2
_main_max_length_before_loop:
    li s2 0
    beq t0 s1 _main_end
    addi s0 s0 4
    lw t1 0(s0)
    addi t0 t0 1
_main_max_length_loop:
    lb t2 0(t1)
    beq t2 zero _main_max_length_mx
    addi s2 s2 1
    addi t1 t1 1
    j _main_max_length_loop
_main_chars:
    mv a0 s5
    call flength
    mv s4 a0
    j _main_end
_main_lines:
    mv a0 s0
    call countlines
    addi s4 a0 -1
_main_end:
    mv a0 s4
    call write_dec
    mv a0 s5
    closef
    exit 0
_main_err:
    exit(1)
