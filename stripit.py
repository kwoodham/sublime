#!/bin/python

import sys
import os
from strip_toc import stripToc

fileName, fileExt = os.path.splitext(str(sys.argv[1]))
fileOut = fileName + '.tmp'
f = open(sys.argv[1], 'r')
a = f.read()
f.close()
a = a.split('\n')
b = stripToc(a)
b = '\n'.join(b)
b = b.lstrip('\n')
f = open(fileOut, 'w')
f.write(b)
f.close()
