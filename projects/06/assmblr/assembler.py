#!/usr/local/bin/python3.8
import sys
import os

from address_hash_table import *
from compute_hash_table import *

def buildSymTable(asmFileStream):
    nextRomAddr = 0

    # Initialize symbols with predifined ones from addresses table
    global symbols
    symbols = {}
    symbols.update(addresses)

    for line in asmFileStream:
        # Ignore all whitespace and comments
        command = line.split("//")[0].rstrip().lstrip()
        if command:
            # Debug printing
            #print(f'{command}    {nextRomAddr}')

            # If command is L type, add symbol and nextRomAddr to symbols
            if command[0] == '(' and command.strip('()') not in symbols:
                symbols[command.strip('()')] = f'{nextRomAddr:016b}'
            # Increment nextRomAddr if command is a C or A type
            else:
                nextRomAddr += 1

    # Debug printing
    #for k,v in symbols.items():
        #print(k,v)

def typeAParse(command):
    # Use hasattr to initialize nextRamAddr as a static variable
    if not hasattr(typeAParse, 'nextRamAddr'):
        typeAParse.nextRamAddr = 16

    command = command.strip('@')
    # Debug printing
    #print(f'A type: {command}')

    # Return command as binary, if it's not an int, check the symbol table
    try:
        return f'{int(command):016b}'
    except ValueError:
        # If it's not in the symbol table, add it
        if command not in symbols:
            symbols[command] = f'{typeAParse.nextRamAddr:016b}'
            typeAParse.nextRamAddr += 1

    return symbols[command]
    
def typeCParse(command):
    # Debug printing
    #print(f'C type: {command}')

    cCmd = {'comp' : None,
             'dest' : 'null',
             'jump' : 'null'}

    # Computation and Jump only
    if not '=' in command:
        (cCmd['comp'], cCmd['jump'])  = command.split(';')
    # Destination and Computation only
    elif not ';' in command:
        (cCmd['dest'], cCmd['comp'])  = command.split('=')
    # All three fields
    else:
        (cCmd['dest'], temp) = command.split('=')
        (cCmd['comp'], cCmd['jump']) = temp.split(';')

    # Debug printing
    #print(f'dest:{cCmd["dest"]}, compt:{cCmd["comp"]}, jump:{cCmd["jump"]}')

    # Build binary using hash tables from compute_hash_table
    return '111' + computations[cCmd['comp']] + destinations[cCmd['dest']] + jumps[cCmd['jump']]

def parseCommand(command):
    # Type A
    if command[0] == '@':
        binary = typeAParse(command)
    # Type L
    elif command[0] == '(':
        # set binary to None, stops line from being output
        binary = None
    # Type C
    else:
        binary = typeCParse(command)

    # Debug printing
    #print(f'binary:{binary}')
    return binary

if __name__ == "__main__":

    asmFile = str(sys.argv[1])

    try:
        asmFileStream = open(asmFile, 'r')
    except FileNotFoundError:
        print('Could not find file: ', asmFile)
    else:
        # Setup the file to write to.  Use same name as input file but with '.hack' extension.
        outFile = os.path.splitext(asmFile)[0] + '.hack'
        outFileStream = open(outFile, 'w')

        # Go through the file once and build the symbol table
        buildSymTable(asmFileStream)

        # Return file reader to top of file, so we can go through it again for command parsing
        asmFileStream.seek(0)

        # Parse assembly file line by line
        for line in asmFileStream:
            # Ignore all whitespace and comments
            command = line.split("//")[0].rstrip().lstrip()
            # If command isn't blank, parse it
            if command:
                # Debug printing
                #print(command)
                binaryLine = parseCommand(command)
                # If it returned something, write it
                if binaryLine:
                    # Debug printing
                    #print(binaryLine)
                    outFileStream.write(binaryLine + '\n')

        # Clean up
        asmFileStream.close()
        outFileStream.close()
