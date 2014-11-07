// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Define location to keep track erase/fill
	@SCREEN
	D=A
	@location
	M=D
// Check if location is outside of SCREEN and if a key is pressed
(CHECK)
	@location
	D=M         // D = location
	@KBD
	D=D-A       // D = location - 24576
	@KEYCHECK
	D;JLT       // If location is within screen size, jump to KEYCHECK
	@SCREEN
	D=A
	@location  	
	M=D    // Else, reset location to first screen address
(KEYCHECK)
	@KBD
	D=M
	@FILL
	D;JNE       // If KBD is not 0, begin filling screen
	@ERASE
	0;JMP       // If KBD is 0, begin erasing

// Fill the screen
(FILL)
	@location
	A=M
	M=-1        // Screen addr. held in location = 0xFF
	@location
	M=M+1       // location++
	@CHECK
	0;JMP       // GOTO CHECK

// Erase the screen
(ERASE)
	@location
	A=M
	M=0         // Screen addr. held in location = 0x00
	@location
	M=M+1       // location++
	@CHECK
	0;JMP       // GOTO CHECK
