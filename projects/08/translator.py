#!/usr/bin/env python3.8

import parser
import codeWriter

import sys
import os

# Get input, single VM file or project directory
vmInput = str(sys.argv[1])

# Parse project name from input, use vm file name without extension or last dir in path
vmProj = os.path.splitext(vmInput)[0]

# Populate list of input .vm files
vmFileArray = []
# Check for a single file being passed
if os.path.isfile(vmInput) and '.vm' in vmInput:
    # Input is a .vm file
    vmFileArray.append(vmInput)
# Check for a directory being passed
elif os.path.isdir(vmInput):
    # Input is a directory, put all .vm files from dir into list
    for file in os.listdir(vmInput):
        if '.vm' in file:
            vmFileArray.append(vmInput + '/' + file)

    # Use directory name as name of asm, at the provided path
    vmProj += '/' + [i for i in os.path.splitext(vmInput)[0].split('/') if i][-1]
else:
    print('Invalid  Input: Provide path to .vm file or directory containing .vm file(s)')
    sys.exit(1)

# If we found vm files, parse and write out the assembly
if len(vmFileArray) > 0:
    # Start writer object with output name
    writer = codeWriter.CodeWriter(vmProj + '.asm')
    # Parse through each file we found
    for vmFile in vmFileArray:
        aParser = parser.Parser(vmFile, writer)
        # parseFile function closes the parser object when finished
        aParser.parseFile()

    # Done with writer, close it up
    writer.close()
else:
    print('No .vm files found')
    sys.exit(1)
