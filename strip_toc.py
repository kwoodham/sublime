#!/bin/python

import sys
import os

# This script takes out the TOC produced by MarkdownTOC and stored the file with a
# ".tmp" extension.  It is called by "panproc" which now puts in a TOC by default.
# The reason I do it this way is that the panproc TOC, when used with "auto_identifiers"
# lets the TOC reference headers that start with numbers (such as 20160309 for today).
# the MarkdownTOc will put ugly identifiers in the text immediately above the header,
# but pandoc then assumes the header line to be a continuation of the preceding line.

fileName, fileExt = os.path.splitext(str(sys.argv[1]))
tempName = fileName+".tmp"

str_beg = '<!-- MarkdownTOC -->\n'
str_end = '<!-- /MarkdownTOC -->\n'

f = open(sys.argv[1], 'r')

a = f.read()
f.close()

f = open(tempName, 'w')
a_loc = a.find(str_beg)

if a_loc > -1:
    f.write(a[:a_loc])
    f.write(a[(a.find(str_end)+len(str_end)+1):])
else:
    f.write(a)
f.close()
