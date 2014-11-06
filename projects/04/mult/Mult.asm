// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

// I'll add R0, R1 times.  
// Copy R1 into R3 so we can jump whem R3 equals zero without out modifying R1
	@R1
	D=M
	@R3
	M=D

	@R2
	M=0    // Initialize R2 to zero

// IF: R3 == 0, END...
(LOOP)
	@R3
	D=M
	@END
	D;JEQ	
// ELSE: R2 = R2 + R0
	@R0
	D=M      // D = R0
	@R2
	M=D+M    // R2 = R0 + R2
	@R3
	M=M-1    // R3--
	@LOOP
	0;JMP    // GOTO LOOP
(END)
	@END
	0;JMP    // Infinite loop ends program
