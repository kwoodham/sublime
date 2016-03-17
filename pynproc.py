#!/usr/bin/python3

import pypandoc
import argparse
import sys
import re
from strip_toc import stripToc

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--notoc", help="No TOC (default)", action="store_true")
parser.add_argument("-t", "--toc", help="Include TOC", action="store_true")
parser.add_argument("-b", "--bib", help="Bibliograpy", metavar='in-file', type=argparse.FileType('rt'),required=False)
parser.add_argument("-i", "--input", help="input file", metavar='in-file', type=argparse.FileType('rt'),required=True)
args = parser.parse_args()

PDOPTS = []
PDOPTS.append('--from=markdown+simple_tables+header_attributes')
PDOPTS.append('--smart')
PDOPTS.append('--standalone')
# PDOPTS.append('--include-in-header=$HOME/css/markdown.css')

if (args.bib):
    PDOPTS.append('--bibliography=' + args.bib + ' --csl ieee')

if (args.toc and args.notoc):
    print("Use either --toc or --notoc (not both). See -h")
    sys.exit()

if (args.toc):
    PDOPTS.append('--toc')


def preProcessMarkups(input_text):

    P = []
    P.append(['\[\[([\w-]+)\]\]', '[\\1](\\1.html)'])  # Links should match [a-zA-Z0-9_-]
    P.append(['.md\)', '.html)'])
    P.append(['.md\#', '.html#'])
    P.append(['.md$', '.html'])

    P.append(['\{\+\+([ \w,.-]+)\+\+\}', '<ins>\\1</ins>'])
    P.append(['\{\-\-([ \w,.-]+)\-\-\}', '<del>\\1</del>'])
    P.append(['\{\=\=([ \w,.-]+)\=\=\}', '<mark>\\1</mark>'])
    P.append(['\{\>\>([ \w,.-]+)\<\<\}', '<span class="critic comment">\\1</span>'])
    P.append(['\{\~\~([ \w,.-]+)\~\>([ \w,.-]+)\~\~\}', '<del>\\1</del><ins>\\2</ins>'])

    f1 = []
    for line in input_text:
        for i in range(0, len(P)):
            line = re.sub(P[i][0], P[i][1], line)
        f1.append(line)

    return f1

in_file = args.input
in_text = in_file.read()
in_text = in_text.split('\n')
in_file.close()

out_text = preProcessMarkups(in_text)
out_text = stripToc(out_text)
out_text = '\n'.join(out_text)

out_html = pypandoc.convert(out_text, to='html', format='md', extra_args=PDOPTS)

print(out_html)
