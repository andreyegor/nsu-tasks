.macro read
	li a7 12 
	ecall
.end_macro

.macro write
	li a7 11
	ecall
.end_macro 

.macro writi %c
	li a0 %c
	write
.end_macro  

.macro exit
	li a7 93
	ecall
.end_macro
