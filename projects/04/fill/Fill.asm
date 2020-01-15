// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Loop through the screens memory space
// for (i=0; i < (256*512); i++)
//   if key pressed
//     fill screen
//   else
//     clear screen

@i
M=0	// initialize i

(LOOP)
@i
D=M	// Hold i in D
@8192	// (256*32)-1
D=D-A
@RESTART
D;JGT	// if i < (256*32) goto RESTART and restart i
	// using jump if i-(256*32-1) > 0
@KBD
D=M	// Hold kbd in D
@CLEAR
D;JEQ	// if kbd == 0 goto CLEAR, else set to black
@i
D=M	// Hold i in D
@SCREEN
A=D+A	// set addr to screen base plus i
M=-1	// fill the current screen word
@INC
0;JMP

(CLEAR)
@i
D=M	// Hold i in D
@SCREEN
A=D+A	// set addr to screen base plus i
M=0	// clear the current screen word

(INC)
@i
M=M+1	// i++
@LOOP
0;JMP	// Loop again

(RESTART)
// Set i back to zero, re-loop through memory space
@i
M=0
@LOOP
0;JMP	// Jump to Loop
