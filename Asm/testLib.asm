#GLOBAL todo maybe better use la a0 smt instead of mv a0 s3-s8

.data
start_msg_1: .asciz "Testing function "
start_msg_2: .asciz "...\n"

failed_msg_1: .asciz "Test is falied: "
#foo(args
failed_msg_2: .asciz ") results in "
#OK(val)/NONE
failed_msg_3: .asciz "expected "
#OK(val)/NONE
ok_open: .asciz "OK("
none: .asciz "NONE"
comma_space: .asciz ", "

#Test falied: foo(str, char) results in OK(int)/NONE, expected OK(int)/NONE

.macro _write_failed_msg %str_in %char_in %int_act, %int_exp #str_test, char_test, (actual, expected) - int, -1 for NONE; all are not a-registers
    la a0 failed_msg_1
    write_str
    mv a0 s1
    write_str
    writi '('
    mv a0 %str_in
    write_str
    la a0 comma_space
    write_str
    mv a0 %char_in
    write
    la a0 failed_msg_2
    write_str
    _write_res %int_act
    writi ' '
    la a0 failed_msg_3
    write_str
    _write_res %int_exp
    writi '\n'
.end_macro


.macro _write_res %int_res #int_res -> int_res!=-1 ? "OK(a0)" | "NONE"
    li a1 -1
    beq %int_res a1 _write_res_none

    la a0 ok_open
    write_str
    mv a0 %int_res
    call write_dec
    writi ')'
    j _write_res_end
_write_res_none:
    la a0 none
    write_str
_write_res_end:
.end_macro

.macro FUNK %foo %name
    .data
        foo_name: .asciz %name
    .text
        la s0 strchr
        la s1 foo_name
        la a0 start_msg_1
        write_str
        la a0 foo_name
        write_str
        la a0 start_msg_2
        write_str
.end_macro

.macro OK %res %line %char
    .data
        line: .asciz %line
    .text
        la a0 line
        li a1 %char
        jalr s0 0

        la t0 line
        li t3 %res
        beq a0 zero none

        sub t2 a0 t0
        bne t2 t3 failed

        addi s2 s2 1
        j end
    failed:
        addi s3 s3 1

        li t1 %char
        _write_failed_msg t0 t1 t2 t3

        j end
    none:
        addi s3 s3 1

        li t1 %char
        li t2 -1
        _write_failed_msg t0 t1 t2 t3
    end:
.end_macro

.macro NONE %line %char
    .data
        line: .asciz %line
    .text
        la a0 line
        li a1 %char
        jalr s0 0

        bne a0 zero failed

        addi s2 s2 1

        j end
    failed:
        addi s3 s3 1

        la t0 line
        li t1 %char
        sub t2 a0 t0
        li t3 -1
        _write_failed_msg t0 t1 t2 t3
    end:
.end_macro

.macro DONE 
    .data
        done_start: .asciz "Passed: "
        done_mid: .asciz ", failed: "
    .text
    la a0 done_start
    write_str
    mv a0 s2
    call write_dec
    la a0 done_mid
    write_str
    mv a0 s3
    call write_dec
    exit(0)
.end_macro
