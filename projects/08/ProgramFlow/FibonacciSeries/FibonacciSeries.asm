// VM Push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// VM Pop pointer 1
@THAT
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// VM Push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// VM Pop that 0
@THAT
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// VM Push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// VM Pop that 1
@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// VM Push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// VM Push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// VM sub
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
D=D-M
@SP
A=M
M=D
@SP
M=M+1
// VM Pop argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Set Label - Function: Sys.main Label: main_loop_start
(Sys.main$main_loop_start)
// VM Push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// If Goto Label - Function: Sys.main Label: compute_element
@SP
M=M-1
A=M
D=M
@Sys.main$compute_element
D;JNE
// Goto Label - Function: Sys.main Label: end_program
@Sys.main$end_program
0;JMP
// Set Label - Function: Sys.main Label: compute_element
(Sys.main$compute_element)
// VM Push that 0
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// VM Push that 1
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// VM add
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
D=D+M
@SP
A=M
M=D
@SP
M=M+1
// VM Pop that 2
@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// VM Push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// VM Push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// VM add
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
D=D+M
@SP
A=M
M=D
@SP
M=M+1
// VM Pop pointer 1
@THAT
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// VM Push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// VM Push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// VM sub
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
D=D-M
@SP
A=M
M=D
@SP
M=M+1
// VM Pop argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Goto Label - Function: Sys.main Label: main_loop_start
@Sys.main$main_loop_start
0;JMP
// Set Label - Function: Sys.main Label: end_program
(Sys.main$end_program)
