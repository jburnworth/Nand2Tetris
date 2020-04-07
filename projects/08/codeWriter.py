#!/usr/bin/env python3.8

import os

from parser import commType as commType

class CodeWriter:
    def __init__(self, asmFileName):
        print(f'output: {asmFileName}\n')
        self.asmFileName = asmFileName
        self.asmStream = open(asmFileName, 'w')
        # Iterators used to make unique names
        self.functionIter = 0
        self.callIter = 0
        self.currentFunc = 'sys.init'

        ## Bootstrap code
        # Set SP=156
        asmStr = '@256\nD=A\n@SP\nM=D\n'
        self.asmStream.write(asmStr)
        # Call Sys.init
        self.writeCall(self.currentFunc, 0)

    def writeFunction(self, name, numArgs):
        print('functionin')
        self.currentFunc = name
        asmStr = f'// Function Def - {name} with {numArgs} argurments\n'
        asmStr += f'({name})\n'
        # Push a 0 to the stack for the number of local arguments
        for i in range(int(numArgs)):
            asmStr += '@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

    def writeCall(self, name, numArgs):
        print('callin')

        num = str(self.callIter)

        asmStr = f'// Calling Function - {name} with {numArgs} arguments\n'
        # Push return address, using label
        asmStr += f'@return{num}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        # Push LCL
        asmStr += '@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        # Push ARG
        asmStr += '@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        # Push THIS
        asmStr += '@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        # Push THAT
        asmStr += '@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        # ARG = SP - n - 5
        asmStr += f'@SP\nD=M\n@{numArgs}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n'
        # LCL = SP
        asmStr += '@SP\nD=M\n@LCL\nM=D\n'
        # Goto f
        asmStr += f'@{name}\n0;JMP\n'
        # Declare lable for return address
        asmStr += f'(return{num})\n'

        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

        self.callIter += 1

    def writeReturn(self):
        print('returnin')
        asmStr = f'// Return call\n'
        # Hold LCL in temp variable FRAME (R13)
        asmStr += '@LCL\nD=M\n@R13\nM=D\n'
        # Hold return address in temp variable RET (FRAME - 5) (R14)
        asmStr += '@5\nD=A\n@R13\nA=M-D\nD=M\n@R14\nM=D\n'
        # Pop from bottom of stack to first ARG, move return value to where it's expected
        asmStr += '@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n'
        # Set SP to ARG + 1
        asmStr += '@ARG\nD=M+1\n@SP\nM=D\n'
        # THAT = FRAME - 1
        asmStr += '@1\nD=A\n@R13\nA=M-D\nD=M\n@THAT\nM=D\n'
        # THIS = FRAME - 2
        asmStr += '@2\nD=A\n@R13\nA=M-D\nD=M\n@THIS\nM=D\n'
        # ARG  = FRAME - 3
        asmStr += '@3\nD=A\n@R13\nA=M-D\nD=M\n@ARG\nM=D\n'
        # LCL  = FRAME - 4
        asmStr += '@4\nD=A\n@R13\nA=M-D\nD=M\n@LCL\nM=D\n'
        # goto RET
        asmStr += '@R14\nA=M\n0;JMP\n'

        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

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

    def writePushPop(self, cType, segment, index, vmFile):
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
                # Store value from static variable in D, use file name to scope variable
                asmStr += f'@{vmFile}.static{str(index)}\nD=M\n'
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
                # Store address of segment base + index in R13
                asmStr += f'@ARG\nD=M\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'local':
                # Store address of segment base + index in R13
                asmStr += f'@LCL\nD=M\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'static':
                # Store address of static variable in R13, use file name to scope variable
                asmStr += f'@{vmFile}.static{str(index)}\nD=A\n@R13\nM=D\n'
            elif segment == 'this':
                # Store address of segment base + index in R13
                asmStr += f'@THIS\nD=M\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'that':
                # Store address of segment base + index in R13
                asmStr += f'@THAT\nD=M\n@{str(index)}\nD=D+A\n@R13\nM=D\n'
            elif segment == 'temp':
                # Store address of segment base + index in R13
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
