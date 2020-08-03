#!/usr/bin/env python3.8

import re

class Tokenizer:
    def __init__(self, jackFile):
        # Initialize class object and open the file
        self.jackFile = jackFile
        self.jackStream = open(self.jackFile, 'r')

    def getTokenDict(self):
        # Read through file, return tuple of tokens, and close file
        tokenz = []
        for line in self.jackStream:
            line = line.split("//")[0].strip()
            if line:
                tokenz.append(line)

        self.jackStream.close()
        return tokenz

>>> for reStr in res:
...     match = re.search(reStr, line)
...     if match:
...             toks.append(match)
