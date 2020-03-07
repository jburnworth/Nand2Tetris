#!/usr/bin/env python3.8

from parser import commType as commType

class CodeWriter:
    def __init__(self, asmFileName):
        print(f'output: {asmFileName}\n')
        self.asmStream = open(asmFileName, 'w')
        self.functionIter = 0

    def writeArithmetic(self, comm):
        print(f'WA: {comm}')

        # Make (small name) variable for uniquely identifying lables
        num = str(self.functionIter)

        if comm == 'neg' or comm == 'not':
            print('unary')
            # Pop into D-register
            asmStr = '@SP\nM=M-1\nA=M\nD=M\n'
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
            asmStr = '@SP\nM=M-1\nA=M\nD=M\n@R13\nM=D\n'
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
            if segment == 'constant':
                asmStr = f'@{str(index)}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        elif cType == commType.cPop:
            print('popin')

        # Write the finished asembly string to the output file
        self.asmStream.write(asmStr)

    def close(self):
        self.asmStream.close()
