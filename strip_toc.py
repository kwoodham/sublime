#!/bin/python

import sys
import os

def stripToc(input):

    # Assume input list split at lines

    str_beg = '<!-- MarkdownTOC -->'
    str_end = '<!-- /MarkdownTOC -->'

    b = []
    toc = False

    for line in input:
        if line == str_beg:
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
