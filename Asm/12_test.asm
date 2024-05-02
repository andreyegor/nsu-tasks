.include "things.asm"
.include "testLib.asm"

.globl main

main:
FUNK strchr_wrapper "strchr"
OK 0 "abcde" "a"
OK 3 "fffwwqw" "w"
OK 2 "abcde" "a"
NONE "abcdef" "Q"
NONE "" "?"
NONE "abcde" "e"
DONE

strchr_wrapper:
    lb a1 0(a1)
    j strchr