#!/usr/bin/env python3.8

import os

from token import Token

class CompliationEngine:
    tokIter = 0
    indentLevel = 0

    def __init__(self, fileName, tokens):
        self.tokens = tokens
        self.xmlOut = open(os.path.splitext(fileName)[0] + '.xml', 'w')
        while (self.tokIter < len(self.tokens)):
            tok = self.getToken()
            #print(f'{tok.type}\t\t{tok.value}')
            if tok.type == 'keyword' and tok.value == 'class':
                self.compileClass(tok)
        self.xmlOut.close()

    # Get next token as long as we're not at the end
    def getToken(self):
        if self.tokIter < len(self.tokens):
            self.tokIter += 1
            return self.tokens[self.tokIter - 1]
        else:
            # TODO should I return a null token?
            return null

    # Write a one-line tag using the token's type and value
    def writeXMLTag(self, token):
        self.xmlOut.write('  ' * self.indentLevel + '<' + token.type + '> ' + token.value + ' </' + token.type + '>\n')

    # TODO Missing subroutineDec or subroutineBody???


    def compileClass(self, tok):
        # Start class tag
        # <class>
        #   <keyword> class </keyword>
        self.xmlOut.write('  ' * self.indentLevel + '<class>\n')
        self.indentLevel += 1
        self.writeXMLTag(tok)
        # Write className
        tok = self.getToken()
        if tok.type == 'identifier':
            self.writeXMLTag(tok)
        else:
            print(f"Error: Expected identifier. Got type {tok.type}: {tok:value}")
            print('\tBet you wish I told you the line number :)')
            sys.exit(2)
        # Write symbol '{'
        tok = self.getToken()
        if tok.type == 'symbol' and tok.value == '{':
            self.writeXMLTag(tok)
        else:
            print(f"Error: expected symbol '{{'. Got {tok.type} {tok.value}")
            print('\tBet you wish I told you the line number :)')
            sys.exit(2)
        # TODO Check for classVarDec or subroutineDec

        # Close class tag
        self.indentLevel -= 1
        self.xmlOut.write('  ' * self.indentLevel + '</class>\n')

    def compileClassVarDec(self):
        True

    def compileSubroutine(self):
        True

    def compileParameterList(self):
        True

    def compileVarDec(self):
        True

    def compileStatements(self):
        True

    def compileDo(self):
        True

    def compileLet(self):
        True

    def compileWhile(self):
        True

    def compileReturn(self):
        True

    def compileIf(self):
        True

    def compileExpression(self):
        True

    def compileTerm(self):
        True

    def compileExpressionList(self):
        True

