#!/usr/bin/env python3.8

import os

from parser import commType as commType

class CodeWriter:
    def __init__(self, asmFileName):
        print(f'output: {asmFileName}\n')
        self.asmFileName = asmFileName
        self.asmStream = open(asmFileName, 'w')
        # Iterator used to make unique names for labels
        self.functionIter = 0
        self.currentFunc = 'Sys.main'

    def writeFunction(self, name, numArgs):
        print('functionin')
        asmStr = f'// Function Def - {name} with {numArgs} argurments\n'
        asmStr += f'({name})\n'
        # Push a 0 to the stack for the number of local arguments
        for i in range(int(numArgs)):
            asmStr += '@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

    def writeReturn(self):
        print('returnin')
        asmStr = f'// Return call\n'
        # Hold LCL in temp variable FRAME
        asmStr += 
        # Hold return address in temp variable RET (FRAME - 5)
        # Pop from bottom of stack to first ARG, move return value to where it's expected
        # Set SP to ARG + 1
        # THAT = FRAME - 1
        # THIS = FRAME - 2
        # ARG  = FRAME - 3
        # LCL  = FRAME - 4
        # goto RET

    def writeLabel(self, label):
        print('labelin')
        # Use notation function$label to scope labels to function
        asmStr = f'// Set Label - Function: {self.currentFunc} Label: {label}\n'
        asmStr += f'({self.currentFunc}${label})\n'
        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

    def writeGoto(self, label):
        print('goto')
        # Use notation function$label to scope labels to function
        asmStr = f'// Goto Label - Function: {self.currentFunc} Label: {label}\n'
        asmStr += f'@{self.currentFunc}${label}\n0;JMP\n'
        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

    def writeIf(self, label):
        print('if-goto')
        # Use notation function$label to scope labels to function
        asmStr = f'// If Goto Label - Function: {self.currentFunc} Label: {label}\n'
        # Pop into D-register
        asmStr += '@SP\nM=M-1\nA=M\nD=M\n'
        # Jump if D isn't zero
        asmStr += f'@{self.currentFunc}${label}\nD;JNE\n'
        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

    def writeArithmetic(self, comm):
        print(f'WA: {comm}')

        # Make a variable (with a short name) for uniquely identifying lables
        num = str(self.functionIter)

        asmStr = f'// VM {comm}\n'
        if comm == 'neg' or comm == 'not':
            print('unary')
            # Pop into D-register
            asmStr += '@SP\nM=M-1\nA=M\nD=M\n'
            # Perform uniary arithemtic opperation on D, store in D
            if comm == 'not':
                asmStr += 'D=!D\n'
            elif comm == 'neg':
                asmStr += 'D=-D\n'
            # Push result in D onto stack
            asmStr += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        else:
            print('binary')
            # Pop into R13
            asmStr += '@SP\nM=M-1\nA=M\nD=M\n@R13\nM=D\n'
            # Pop into D-register
            asmStr += '@SP\nM=M-1\nA=M\nD=M\n'

            # Perform arithmetic opperation on R13 and D, store in D
            if comm == 'add':
                asmStr += '@R13\nD=D+M\n'
            elif comm == 'sub':
                asmStr += '@R13\nD=D-M\n'
            elif comm == 'eq':
                asmStr += f'@R13\nD=D-M\n@TRUE{num}\nD;JEQ\nD=0\n@DONE{num}\n0;JMP\n(TRUE{num})\nD=-1\n(DONE{num})\n'
            elif comm == 'gt':
                asmStr += f'@R13\nD=D-M\n@TRUE{num}\nD;JGT\nD=0\n@DONE{num}\n0;JMP\n(TRUE{num})\nD=-1\n(DONE{num})\n'
            elif comm == 'lt':
                asmStr += f'@R13\nD=D-M\n@TRUE{num}\nD;JLT\nD=0\n@DONE{num}\n0;JMP\n(TRUE{num})\nD=-1\n(DONE{num})\n'
            elif comm == 'and':
                asmStr += '@R13\nD=D&M\n'
            elif comm == 'or':
                asmStr += '@R13\nD=D|M\n'

            # Push result in D onto stack
            asmStr += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'

            # Increment function iterator
            self.functionIter += 1

        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

    def writePushPop(self, cType, segment, index):
        print(f'PP: {cType} {segment} {index}')
        if cType == commType.cPush:
            print('pushin')
            asmStr = f'// VM Push {segment} {index}\n'
            if segment == 'constant':
                # Store constant in D
                asmStr += f'@{str(index)}\nD=A\n'
            elif segment == 'argument':
                # Store value from segment base + index in D
                asmStr += f'@ARG\nD=M\n@{str(index)}\nA=D+A\nD=M\n'
            elif segment == 'local':
                # Store value from segment base + index in D
                asmStr += f'@LCL\nD=M\n@{str(index)}\nA=D+A\nD=M\n'
            elif segment == 'static':
                # Store value from segment base + index in D
                asmStr += f'@16\nD=A\n@{str(index)}\nA=D+A\nD=M\n'
            elif segment == 'this':
                # Store value from segment base + index in D
                asmStr += f'@THIS\nD=M\n@{str(index)}\nA=D+A\nD=M\n'
            elif segment == 'that':
                # Store value from segment base + index in D
                asmStr += f'@THAT\nD=M\n@{str(index)}\nA=D+A\nD=M\n'
            elif segment == 'temp':
                # Store value from segment base + index in D
                asmStr += f'@R5\nD=A\n@{str(index)}\nA=D+A\nD=M\n'
            elif segment == 'pointer':
                if index == '0':
                    # Store base of THIS in D
                    asmStr += '@THIS\nD=M\n'
                elif index == '1':
                    # Store base of THAT in D
                    asmStr += '@THAT\nD=M\n'
            # Push result in D onto stack
            asmStr += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        elif cType == commType.cPop:
            print('popin')
            asmStr = f'// VM Pop {segment} {index}\n'
            if segment == 'argument':
                # Store segment base + index in R13
                asmStr += f'@ARG\nD=M\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'local':
                # Store segment base + index in R13
                asmStr += f'@LCL\nD=M\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'static':
                # Store segment base + index in R13
                asmStr += f'@16\nD=A\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'this':
                # Store segment base + index in R13
                asmStr += f'@THIS\nD=M\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'that':
                # Store segment base + index in R13
                asmStr += f'@THAT\nD=M\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'temp':
                # Store segment base + index in R13
                asmStr += f'@R5\nD=A\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'pointer':
                if index == '0':
                    # Store address of THIS in R13
                    asmStr += '@THIS\nD=A\n@R13\nM=D\n'
                elif index == '1':
                    # Store address of THAT in R13
                    asmStr += '@THAT\nD=A\n@R13\nM=D\n'
            # Pop into D-register
            asmStr += '@SP\nM=M-1\nA=M\nD=M\n'
            # Write D to location address held in R13
            asmStr += '@R13\nA=M\nM=D\n'

        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

    def close(self):
        self.asmStream.close()
