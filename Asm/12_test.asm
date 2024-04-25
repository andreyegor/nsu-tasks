.include "testLib.asm"
.text
.include "things.asm"
.include "12.asm"

.globl main

main:
FUNK strchr "strchr"
OK 0 "abcde" 'a'
OK 3 "fffwwqw" 'w'
OK 2 "abcde" 'a'
NONE "abcdef" 'Q'
NONE "" '?'
NONE "abcde" 'e'
DONE
