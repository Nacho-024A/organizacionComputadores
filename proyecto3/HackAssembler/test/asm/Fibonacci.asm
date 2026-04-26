// Calcula los primeros N números de Fibonacci
// N = 6

@6
D=A
@N
M=D        // N = 6

@0
D=A
@A
M=D        // A = 0

@1
D=A
@B
M=D        // B = 1

(LOOP)
@N
D=M
@END
D;JEQ      // Si N == 0 → fin

@A
D=M
@OUTPUT
M=D        // Guarda resultado actual

@A
D=M
@B
D=D+M      // D = A + B

@TEMP
M=D        // TEMP = A + B

@B
D=M
@A
M=D        // A = B

@TEMP
D=M
@B
M=D        // B = TEMP

@N
M=M-1      // N--

@LOOP
0;JMP

(END)
@END
0;JMP