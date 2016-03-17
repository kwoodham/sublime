#!/bin/python

# 17 Mar 2016 - Python version of my "panproc" bash script - uses the python argument
# parser to be a bit more flexible. This file preprocess the Markdown for critic marks,
# stripping out the MarkdownTOC (toc swtich can put in an html version), and adds anchors
# for internal links with headings that start with digits.

import pypandoc
import argparse
import sys
import re
import os.path
from strip_toc import stripToc
from add_anchors import addAnchors


def preProcessMarkups(input_text):

    P = []
    P.append(['\[\[([\w-]+)\]\]', '[\\1](./\\1.html)'])  # Links should match [a-zA-Z0-9_-]
    P.append(['.md\)', '.html)'])
    P.append(['.md\#', '.html#'])
    P.append(['.md$', '.html'])

    P.append(['\{\+\+([\S\s]+?)\+\+\}', '<ins>\\1</ins>'])
    P.append(['\{\-\-([\S\s]+?)\-\-\}', '<del>\\1</del>'])
    P.append(['\{\=\=([\S\s]+?)\=\=\}', '<mark>\\1</mark>'])
    P.append(['\{\>\>([\S\s]+?)\<\<\}', '<span class="critic comment">\\1</span>'])
    P.append(['\{\>\>\<\<\}', '<span class="critic comment"></span>'])
    P.append(['\{\~\~([\S\s]+?)\~\>([\S\s]+?)\~\~\}', '<del>\\1</del><ins>\\2</ins>'])

    f1 = []
    for line in input_text:
        for i in range(0, len(P)):
            line = re.sub(P[i][0], P[i][1], line)
        f1.append(line)

    return f1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--notoc", help="No TOC (default)", action="store_true")
    parser.add_argument("-t", "--toc", help="Include TOC", action="store_true")
    parser.add_argument("-b", "--bib", help="Bibliograpy", metavar='in-file', type=argparse.FileType('rt'),required=False)
    parser.add_argument("-i", "--input", help="input file", metavar='in-file', type=argparse.FileType('rt'),required=True)
    parser.add_argument("-o", "--output", help="output file (default is input.html)", type=str,required=False )
    args = parser.parse_args()

    PDOPTS = []
    PDOPTS.append('--from=markdown+simple_tables+auto_identifiers')  # These might be default anyhow
    PDOPTS.append('--smart')
    PDOPTS.append('--standalone')
    PDOPTS.append('--include-in-header=' + os.path.expanduser('~') + '/css/markdown.css')

    if (args.bib):
        PDOPTS.append('--bibliography=' + args.bib + ' --csl ieee')

    if (args.toc and args.notoc):
        print("Use either --toc or --notoc (not both). See -h")
        sys.exit()

    if (args.toc):
        PDOPTS.append('--toc')

    if (not args.output):
        args.output = args.input.name.split('.')[0] + '.html'

    in_file = args.input
    in_text = in_file.read()
    in_text = in_text.split('\n')
    in_file.close()

    out_text = preProcessMarkups(in_text)
    out_text = stripToc(out_text)
    out_text = addAnchors(out_text)

    out_text = '\n'.join(out_text)

    out_html = pypandoc.convert(
        out_text,
        to='html', format='md',
        outputfile=args.output,
        extra_args=PDOPTS)

    # Take out offending style line put in by pandoc - written out to
    # a file, so we have to read it back in.
    # UTF-8 encoding require to support --smart switch on pandoc.

    f = open(args.output, 'r', encoding='utf-8')
    a = f.read()
    f.close()
    loc_beg = a.find('  <style type="text/css">')
    loc_end = a.find('</style>', loc_beg) + int(9)  # length of the close tag + 1 space
    f = open(args.output, 'w', encoding='utf-8')
    f.write(a[:loc_beg] + a[loc_end:])
    f.close()
