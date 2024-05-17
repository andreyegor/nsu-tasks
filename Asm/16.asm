.include "things.asm"
.data
ext: .asciz ".sorted"

.text
.globl main

main:
    beq a0 zero _main_err
    lw s11 0(a1)
    la s10 ext
    mv a0 s11
    li a1 0
    call fopen
    mv s1 a0
    call fload
    mv s0 a0
    mv a0 s1
    closef

    mv a0 s0
    call splitlines
    mv s1 a0

    call msd_sort
    mv s2 a0

    mv a0 s11
    call strlen
    mv a0 s3
    mv a0 s10
    call strlen
    add s3 s3 a0
    sub sp sp s3
    mv s9 sp
    mv a1 sp
    mv a0 s11
    call strcopy
    addi a1 a0 -1
    mv a0 s10
    call strcopy

    mv a0 s9
    li a1 1
    call fopen
    mv s1 a0

    add sp sp s3
    lw s3 0(s2)
    addi s3 s3 -1
_main_write_loop:
    addi s2 s2 4
    mv a0 s1
    lw a1 0(s2)
    call fwriteline_break

    addi s3 s3 -1
    bne s3 zero _main_write_loop
    addi s2 s2 4
    mv a0 s1
    lw a1 0(s2)
    call fwriteline
_main_continue:
    mv a0 s1
    closef
    exit(0)
_main_err:
    exit(1)


msd_sort: #[length, lines...] -> same array
    push_2 ra a0
    addi a1 a0 4
    lw a0 0(a0)
    li a2 0
    call msd_sort_re
    pop_2 ra a0
    ret

msd_sort_re: #length, lines, sign no -> none, in array is changed
    li t0 1
    ble a0 t0 _msd_sort_re_quit

    addi sp sp -1024 #255 ints
    mv t1 sp #counter
    slli t0 a0 4
    sub sp sp t0
    mv t0 sp #new arr

    li t2 255 #iterate
    mv t3 t1 #now
_msd_sort_re_zeros_loop:
    sw zero 0(t3)
    addi t2 t2 -1
    addi t3 t3 4
    bne t2 zero _msd_sort_re_zeros_loop

    mv t2 a0 #iterate
    mv t3 a1 #line now
_msd_sort_re_count_loop:
    lw t4 0(t3)

    addi t2 t2 -1
    addi t3 t3 4

    add t4 t4 a2
    lb t4 0(t4)

    add t5 t1 t4
    add t5 t5 t4
    add t5 t5 t4
    add t5 t5 t4

    lw t4 0(t5)
    addi t4 t4 1
    sw t4 0(t5)

    bne t2 zero _msd_sort_re_count_loop

    li t2 255 #iterate
    mv t3 t1 #now
    li t4 0 #prev
_msd_sort_re_other_count_loop:
    lw t5 0(t3)
    add t4 t4 t5
    sw t4 0(t3)

    addi t2 t2 -1
    addi t3 t3 4
    bne t2 zero _msd_sort_re_other_count_loop

    mv t2 a0 #iterate
    mv t3 a1 #line now
_msd_sort_re_sort_itself_loop:
    lw t4 0(t3)

    add t4 t4 a2
    lb t4 0(t4)

    add t5 t1 t4
    add t5 t5 t4
    add t5 t5 t4
    add t5 t5 t4

    lw t4 0(t5)
    addi t4 t4 -1
    sw t4 0(t5)

    slli t6 t4 2
    add t6 t6 t0


    lw t4 0(t3)
    sw t4 0(t6)

    addi t2 t2 -1
    addi t3 t3 4
    bne t2 zero _msd_sort_re_sort_itself_loop

    mv t2 a0 #iterate
    mv t3 a1 #line now
    mv t4 t0 #line now
_msd_sort_re_move_data_loop:
    lw t5 0(t4)
    sw t5 0(t3)

    addi t2 t2 -1
    addi t3 t3 4
    addi t4 t4 4
    bne t2 zero _msd_sort_re_move_data_loop
    slli t2 a0 4
    add sp sp t2 #free stack

    push ra
    li t2 254 #iterate
    lw t4 0(t1) #prev
    addi t3 t1 4 #now
_msd_sort_re_recursion_loop:
    mv t5 t4
    lw t4 0(t3)
    sub t6 t4 t5
    beq t6 zero _msd_sort_re_recursive_loop_end 
    push_6 a0 a1 a2 t2 t3 t4
    mv a0 t6
    slli t5 t5 2
    add a1 a1 t5
    addi a2 a2 1
    call msd_sort_re
    pop_6 a0 a1 a2 t2 t3 t4
_msd_sort_re_recursive_loop_end:
    addi t2 t2 -1
    addi t3 t3 4
    bne t2 zero _msd_sort_re_recursion_loop

    pop ra
    addi sp sp 1024 #free stack
_msd_sort_re_quit:
    ret
