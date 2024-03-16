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
