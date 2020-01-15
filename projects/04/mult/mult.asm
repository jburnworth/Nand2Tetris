// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// for (i=1; i <= R1; i++)
//   R2 += R0

@R2
M=0	// Initialize R2 to 0
@i
M=1	// We'll use i as the iterator in the for loop

(LOOP)
@i
D=M	// Hold i in D
@R1	// Load the value of R1 in M
D=D-M	// D=i-R1
@END
D;JGT	// if (i-R1)>0 goto END
@R0
D=M	// Hold R0 in D
@R2
M=D+M	// R2 = R0 + R2
@i
M=M+1	// i++
@LOOP
0;JMP	// repeat

(END)
@END
0;JMP	// End of program infinite loop
