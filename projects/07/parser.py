#!/usr/local/bin/python3.8

import re
from enum import Enum, unique, auto

class Parser:
    def __init__(self, vmFile):
        self.vmFile = vmFile
        self.cType = None
    
    def arg1(self, comm):
        if self.cType != commType.cArithmetic:
            return comm.split()[1]
        else:
            return comm.split()[0]

    def arg2(self, comm):
        return comm.split()[2]

    # Return the command type
    def commandType(self, comm):
        if comm:

            # Make sure it's lower case so we aren't bamboozeled
            comm = comm.lower()
            # Create regular expresions for each command type
            rePush = re.compile('^push')
            rePop = re.compile('^pop')
            reLabel = re.compile('^label')
            reGoto = re.compile('^goto')
            reIf = re.compile('^if')
            reFunction = re.compile('^function')
            reReturn = re.compile('^return')
            reCall = re.compile('^call')

            # Use the first word in the command to figure out what type it is
            if rePush.match(comm):
                return commType.cPush
            elif rePop.match(comm):
                return commType.cPop
            elif reLabel.match(comm):
                return commType.cLabel
            elif reGoto.match(comm):
                return commType.cGoto
            elif reIf.match(comm):
                return commType.cIf
            elif reFunction.match(comm):
                return commType.cFunction
            elif reReturn.match(comm):
                return commType.cReturn
            elif reCall.match(comm):
                return commType.cCall
            # Else it's arithmetic!:
            else:
                return commType.cArithmetic

    def parseFile(self):
        if self.vmFile:
            vmStream = open(self.vmFile, 'r')

            for line in vmStream:
                comm = line.split("//")[0].strip() 
                if comm:
                    argu1 = None
                    argu2 = None
                    callArg2 = {commType.cPush, commType.cPop, commType.cFunction, commType.cCall}
                    self.cType = self.commandType(comm)
                    if self.cType != commType.cReturn:
                        argu1 = self.arg1(comm)
                    if self.cType in callArg2:
                        argu2 = self.arg2(comm)
                    print(f'{comm}\n\t{self.cType}\ta1:{argu1}\ta2:{argu2}')

@unique
class commType(Enum):
    cArithmetic = auto()
    cPush = auto()
    cPop = auto()
    cLabel = auto()
    cGoto = auto()
    cIf = auto()
    cFunction = auto()
    cReturn = auto()
    cCall = auto()
