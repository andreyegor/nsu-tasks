strchr: #nullt str ptr, char -> ptr in str/null
    lb t0 0(a0)
    addi a0 a0 1
    beq t0 zero _strchr_err
    bne t0 a1 strchr

    addi a0 a0 -1
    ret
_strchr_err:
    li a0 0
    ret
