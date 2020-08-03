#!/usr/bin/env python3.8

import tokenizer
#import compilation

import sys, os

# Get input, single .jack file or directory containing .jack file(s)
try:
    projectInput = str(sys.argv[1])
except:
    print('Please pass one argument, the path to a .jack file or a directory containing .jack files')
    sys.exit(1)

# Parse project name from input
# If a file, use file name without .jack extension,
# if a directory, use last directory in path
project = os.path.splitext(projectInput)[0]

# Find all the files we need to analyze
jackFileArray = []
# Check if single file is passed
if os.path.isfile(projectInput) and '.jack' in projectInput:
    jackFileArray.append(projectInput)
# Or check if a directory is passed
elif os.path.isdir(projectInput):
    for file in os.listdir(projectInput):
        if '.jack' in file:
            jackFileArray.append(projectInput + '/' + file)

# Check if any .jack files were found
if len(jackFileArray) < 1:
    print('No .jack files found: Pass path to a .jack file or a directory containing .jack files')
    sys.exit(1)

# Analyze found .jack files
for jackFile in jackFileArray:
    # Tokenize the file.
    aTokenizer = tokenizer.Tokenizer(jackFile)
    tokenz = aTokenizer.getTokenDict()

    # Write tokens as xml file
    xmlOut = open(os.path.splitext(jackFile)[0] + '.xml', 'w')
    for token in tokenz:
        xmlOut.write(token + '\n')
    xmlOut.close()

    # Compile tokens
