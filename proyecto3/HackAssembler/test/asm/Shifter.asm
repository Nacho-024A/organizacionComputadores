// Test Shifter
// Prueba shift left: D = 1, luego D = D << 1 (esperado: 2)
@1
D=A
D=D<<1
@R0
M=D

// Prueba shift right: D = 4, luego D = D >> 1 (esperado: 2)
@4
D=A
D=D>>1
@R1
M=D

// Prueba shift left desde memoria: M[2] = 3, D = M << 1 (esperado: 6)
@3
D=A
@R2
M=D
@R2
D=M
D=D<<1
@R3
M=D

// Prueba shift right con numero impar: D = 5 >> 1 (esperado: 2, se pierde el bit)
@5
D=A
D=D>>1
@R4
M=D

// Fin
@END
(END)
0;JMP