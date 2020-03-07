#!/usr/bin/env python3.8

import parser
import codeWriter

import sys
import os

vmProj = str(sys.argv[1])

writer = codeWriter.CodeWriter(os.path.splitext(vmProj)[0] + '.asm')

par1 = parser.Parser(vmProj, writer)
par1.parseFile()

writer.close()
