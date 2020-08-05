#!/usr/bin/env python3.8

import re
from lexicalElements import jackKeywords, jackSymbols

class Tokenizer:
    def __init__(self, jackFile):
        # Initialize class object and open the file
        self.jackFile = jackFile
        self.jackStream = open(self.jackFile, 'r')

    # Read through file, return tuple of tokens, and close file
    def getTokenDict(self):
        ## Regex definitions
        # Regex to match jack strings, unicode chars between ""
        jackStringsRe = re.compile(r'["\']([^"\']+)["\']')
        # Regex to match jack symbols
        jackSymbolsRe = re.compile(fr"({'|'.join([re.escape(char) for char in jackSymbols])})")
        # Match comments like /*...*/ using non-greedy regex with '.' matching
        # everything, including newlines (DOTALL)
        multiLineCommentRe = re.compile(r'\/\*.*?\*\/', re.DOTALL)

        # Read whole file into a string
        fileText = self.jackStream.read()
        # Remove multi-line comments with regex substitution
        fileText = multiLineCommentRe.sub('', fileText)

        # Append tokens to this list as we go through the file
        tokenz = []
        # Parse file text line by line
        for line in fileText.splitlines():
            # Remove leading and trailing white space and normal comments (//)
            line = line.split("//")[0].strip()
            if line:
                # Step 1: Preserve strings by turning line into a list, splitting by strings
                stringSplit = jackStringsRe.split(line)
                # Step 2: Create list of just strings to compare with later
                stringToks = jackStringsRe.findall(line)
                # Step 3: Go through line list, tokenizing anything that is not already a string token
                for str in stringSplit:
                    if str in stringToks:
                        tokenz.append([str])
                    else:
                        for tok in str.split():
                            tokenz.append(list(t for t in jackSymbolsRe.split(tok) if t))

        # Flatten list
        tokenz = sum(tokenz, [])
        for z in tokenz:
            print(z)
        #print(tokenz)
        self.jackStream.close()
        return tokenz
