#!/usr/local/bin/python3.8

import parser
import codeWriter

import sys

vmProj = str(sys.argv[1])

par1 = parser.Parser(vmProj)
par1.parseFile()

