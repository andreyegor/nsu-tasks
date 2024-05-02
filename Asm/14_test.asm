.include "things.asm"
.include "testLib.asm"

.globl main

main:
FUNK strstr "strstr"
OK 3 "123abobab4567890" "aboba"
OK 5 "333ababoba33" "aboba"
NONE "222abob2" "aboba"
NONE "55boba55" "aboba"
NONE "adsd" "aboba"
DONE
