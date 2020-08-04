#!/usr/bin/env python3.8

import re
from lexicalElements import jackKeywords, jackSymbols

class Tokenizer:
    def __init__(self, jackFile):
        # Initialize class object and open the file
        self.jackFile = jackFile
        self.jackStream = open(self.jackFile, 'r')

    def getTokenDict(self):
        # Read through file, return tuple of tokens, and close file
        # Regex to match jack strings, unicode chars between ""
        jackStringsRe = re.compile(r'["\']([^"\']+)["\']')
        # Regex to match jack symbols
        jackSymbolsRe = re.compile(fr"({'|'.join([re.escape(char) for char in jackSymbols])})")

        # Append tokens to this list as we go through the file
        tokenz = []
        # TODO Remove multi-line comments
        for line in self.jackStream:
            # Remove leading and trailing line spaces and normal comments (//)
            line = line.split("//")[0].strip()
            if line:
                # Step 1: Preserve strings byt turning line into a list, splitting by strings
                stringSplit = jackStringsRe.split(line)
                # Step 2: Create list of just strings to compare with later
                stringToks = jackStringsRe.findall(line)
                print(f'Line split by strings: {stringSplit}')
                # Step 3: Go through line list, tokenizing anything that is not a string
                for str in stringSplit:
                    if str in stringToks:
                        tokenz.append([str])
                    else:
                        for tok in str.split():
                            tokenz.append(list(t for t in jackSymbolsRe.split(tok) if t))

        tokenz = sum(tokenz, [])
        for z in tokenz:
            print(z)
        #print(tokenz)
        self.jackStream.close()
        return tokenz
