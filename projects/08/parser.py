#!/usr/bin/env python3.8

import re
from enum import Enum, unique, auto

class Parser:
    def __init__(self, vmFileName, codeRightr):
        self.vmFileName = vmFileName
        self.codeRightr = codeRightr
    
    def argu1(self, comm, cType):
        if cType != commType.cArithmetic:
            return comm.split()[1]
        else:
            return comm.split()[0]

    def argu2(self, comm):
        return comm.split()[2]

    # Return the command type
    def commandType(self, commLine):
        if commLine:

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
            if rePush.match(commLine):
                return commType.cPush
            elif rePop.match(commLine):
                return commType.cPop
            elif reLabel.match(commLine):
                return commType.cLabel
            elif reGoto.match(commLine):
                return commType.cGoto
            elif reIf.match(commLine):
                return commType.cIf
            elif reFunction.match(commLine):
                return commType.cFunction
            elif reReturn.match(commLine):
                return commType.cReturn
            elif reCall.match(commLine):
                return commType.cCall
            # Else it's arithmetic!:
            else:
                return commType.cArithmetic

    def parseFile(self):
        if self.vmFileName:
            self.vmStream = open(self.vmFileName, 'r')

            for line in self.vmStream:
                commLine = line.split("//")[0].strip() 
                if commLine:
                    # Make sure it's lower case so we aren't bamboozeled
                    commLine = commLine.lower()

                    # Determine the command type
                    cType = self.commandType(commLine)

                    # Turn the command into a list to store in appropriate variables
                    commList = commLine.split()
                    # Pad command list with 'None' in case it's too short
                    comLength = 3
                    (command, arg1, arg2) = commList[:comLength] + [None]*(comLength-len(commList))

                    if cType == commType.cArithmetic:
                        # Write out arithmetic command
                        self.codeRightr.writeArithmetic(command)
                    elif cType == commType.cPush or cType == commType.cPop:
                        # Write out push or pop command
                        self.codeRightr.writePushPop(cType, arg1, arg2)
                    elif cType == commType.cLabel:
                        # Call write label and pass arg1, the label name
                        self.codeRightr.writeLabel(arg1)
                    elif cType == commType.cGoto:
                        # Call write goto and pass arg1, the label name
                        self.codeRightr.writeGoto(arg1)
                    elif cType == commType.cIf:
                        # Call write if-goto and pass arg1, the label name
                        self.codeRightr.writeIf(arg1)
                    elif cType == commType.cFunction:
                        # Call write function and pass arg1, function name, and arg2, num of func args
                        self.codeRightr.writeFunction(arg1, arg2)

            self.close()

    def close(self):
        self.vmStream.close()

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
