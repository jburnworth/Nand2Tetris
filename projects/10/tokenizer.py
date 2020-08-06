#!/usr/bin/env python3.8

import re
from token import Token
from lexicalElements import jackKeywords, jackSymbols

class Tokenizer:
    def __init__(self, jackFile):
        # Initialize class object and open the file
        self.jackFile = jackFile
        self.jackStream = open(self.jackFile, 'r')

    # Read through file, return tuple of tokens, and close file
    def getTokenDict(self):

        # Quick helper function for testing if a token (string) is an int
        def representsInt(s):
            try:
                int(s)
                return True
            except ValueError:
                return False

        ## Regex definitions
        # Regex to match jack strings, unicode chars between ""
        jackStringsRe = re.compile(r'["\']([^"\']+)["\']')
        # Regex to match jack symbols
        jackSymbolsRe = re.compile(fr"({'|'.join([re.escape(char) for char in jackSymbols])})")
        # Match comments like /*...*/ using non-greedy regex with '.' matching
        # everything, including newlines (DOTALL)
        multiLineCommentRe = re.compile(r'\/\*.*?\*\/', re.DOTALL)

        # Read whole file into a string then close file
        fileText = self.jackStream.read()
        self.jackStream.close()
        # Remove multi-line comments with regex substitution
        fileText = multiLineCommentRe.sub('\n', fileText)

        # Split file up into tokens and store in a list for further parsing
        tokenz = []
        stringToks = []
        # Parse file text line by line
        for line in fileText.splitlines():
            # Remove leading and trailing white space and normal comments (//)
            line = line.split("//")[0].strip()
            if line:
                # Step 1: Preserve strings by turning line into a list, splitting by strings
                stringSplit = jackStringsRe.split(line)
                # Step 2: Create list of just strings to compare with later
                stringTokTemps = jackStringsRe.findall(line)
                stringToks.append(stringTokTemps)
                # Step 3: Go through line list, tokenizing anything that is not already a string token
                for str in stringSplit:
                    if str in stringTokTemps:
                        tokenz.append([str])
                    else:
                        for tok in str.split():
                            tokenz.append(list(t for t in jackSymbolsRe.split(tok) if t))

        # Flatten lists
        tokenz = sum(tokenz, [])
        stringToks = sum(stringToks, [])

        # Type the tokens, creating list of token objects
        # regex to match int_const, 0..32767
        intConstRe = re.compile(r'\d|[1-9]\d|[1-9]\d\d|[1-9]\d\d\d|[1-9]\d')
        tokenList = []
        for tok in tokenz:
            if tok in jackKeywords:
                tokenList.append(Token('keyword', tok))
            elif tok in jackSymbols:
                tokenList.append(Token('symbol', tok))
            elif tok in stringToks:
                tokenList.append(Token('string_const', tok))
            elif representsInt(tok):
                if int(tok) in range(0,32767):
                    tokenList.append(Token('int_const', tok))
                else:
                    print(f'Error: Int {tok} out of range (0..32767)')
            else:
                tokenList.append(Token('identifier', tok))

        #for z in tokenz:
            #print(z)
        print('Token List:')
        for z in tokenList:
            print(f'{z.type}\t\t{z.value}')
        #print(tokenz)
        return tokenList
