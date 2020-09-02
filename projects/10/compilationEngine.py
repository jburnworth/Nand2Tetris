#!/usr/bin/env python3.8

import os
import sys

from token import Token

class CompliationEngine:
    tokIter = 0
    indentLevel = 0

    def __init__(self, fileName, tokens):
        self.tokens = tokens
        self.xmlOut = open(os.path.splitext(fileName)[0] + '.xml', 'w')
        # Start parsing the token list
        while (self.tokIter < len(self.tokens)):
            tok = self.getToken()
            #print(f'{tok.type}\t\t{tok.value}')
            # First check for a class declaration
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
            print('\tBet you wish I told you the line number :P')
            sys.exit(2)
        # Write symbol '{'
        tok = self.getToken()
        if tok.type == 'symbol' and tok.value == '{':
            self.writeXMLTag(tok)
        else:
            print(f"Error: expected symbol '{{'. Got {tok.type} {tok.value}")
            print('\tBet you wish I told you the line number :P')
            sys.exit(2)
        # Check for classVarDec(s)
        tok = self.getToken()
        while (tok.type == 'keyword' and (tok.value == 'static' or tok.value == 'field')):
            self.compileClassVarDec(tok)
            # get next token to see if there is another callVarDec
            tok = self.getToken()
        
        # TODO Check for subroutineDec

        # Close class tag
        self.indentLevel -= 1
        self.xmlOut.write('  ' * self.indentLevel + '</class>\n')

    def compileClassVarDec(self, tok):
        # Start classVarDec tag
        self.xmlOut.write('  ' * self.indentLevel + '<classVarDec>\n')
        self.indentLevel += 1
        # Write scope, static or field
        self.writeXMLTag(tok)
        # Write type
        tok = self.getToken()
        if tok.type == 'keyword':
            self.writeXMLTag(tok)
        else:
            print(f"Error: expected keyword for variable type. Got {tok.type} {tok.value}")
            print('\tBet you wish I told you the line number :P')
            sys.exit(2)
        # Write variable name
        tok = self.getToken()
        if tok.type == 'identifier':
            self.writeXMLTag(tok)
        else:
            print(f"Error: expected identifier for variable name. Got {tok.type} {tok.value}")
            print('\tBet you wish I told you the line number :P')
            sys.exit(2)
        # Check for list of variables
        tok = self.getToken()
        while (tok.type == 'symbol' and tok.value == ','):
            # Write comma
            self.writeXMLTag(tok)
            # Write variable name
            tok = self.getToken()
            if tok.type == 'identifier':
                self.writeXMLTag(tok)
            else:
                print(f"Error: expected identifier for variable name. Got {tok.type} {tok.value}")
                print('\tBet you wish I told you the line number :P')
                sys.exit(2)
            # Get next token to see if there is another variable name in the list
            tok = self.getToken()
        # ClassVarDec ends with a ;
        if tok.type == 'symbol' and tok.value == ';':
            self.writeXMLTag(tok)
        else:
            print(f"Error: expected symbol ';'. Got {tok.type} {tok.value}")
            print('\tBet you wish I told you the line number :P')
            sys.exit(2)
        # Close classVarDec tag
        self.indentLevel -= 1
        self.xmlOut.write('  ' * self.indentLevel + '</classVarDec>\n')
        

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

