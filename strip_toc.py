#!/bin/python

import sys
import os

# 9/22/2019 - sometimes additional switches are placed in the header, so
# just match on the part of the header that doesn't change

def stripToc(input):

    # Assume input list split at lines

    str_beg = '<!-- MarkdownTOC'
    str_end = '<!-- /MarkdownTOC -->'

    b = []
    toc = False

    for line in input:
        if line[:len(str_beg)] == str_beg:
            toc = True
        elif line == str_end:
            toc = False
            continue
        if (not toc):
            b.append(line)
    return b

if __name__ == '__main__':
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
