.include "things.asm"
.text
.globl main
main:
    call read_dec
    call write_dec
    exit 0