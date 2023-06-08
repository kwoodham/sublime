#!/mingw64/bin/python

# 6/8/2023
# MingW64 had trouble with timestamp popen() - so implemented different
# method to put modification time at end of file

# 6/7/2023
# Use re on out_html to change \r\n to \n. This took double spaced lines out of output
# which had the effect of including the extra lines in codeblocks.

# 4/25/2019
# Use top heading to name page in browser

# 10 April 2019
# - added check to see if html output file existed and delete it if so. 
# (Seems like there were instances where some output files had some updates appended to
# existing files.)
# - Update pyndoc.convert() to pyndoc.convert_text() per deprecated function warnings.
# It looks like this expects to return text, so had to add in explicit write of returned
# text to file
# - Looks like pandoc no longer includes offending <style> stuff that I had to cut out
# before - can now dump pandoc converted text directly to output file

# 17 Mar 2016 - Python version of my "panproc" bash script - uses the python argument
# parser to be a bit more flexible. This file preprocesses the Markdown for critic marks,
# stripping out the MarkdownTOC (toc switch can put in an html version), and adds anchors
# for internal links with headings that start with digits.

import pypandoc
import argparse
import datetime
import sys
import re
import os
from strip_toc import stripToc
from add_anchors import addAnchors


def preProcessMarkups(input_text):

    P = []

    # Wiki-style links, and links to other Markdown files (with or without anchors)
    P.append(['\[\[([\w-]+)\]\]', '[\\1](./\\1.html)'])  # Links should match [a-zA-Z0-9_-]
    P.append(['.md\)', '.html)'])
    P.append(['.md\#', '.html#'])
    P.append(['.md$', '.html'])

    # Critic markups (1) pattern (2) html-show
    P.append(['\{\+\+([\S\s]+?)\+\+\}', '<ins>\\1</ins>'])
    P.append(['\{\-\-([\S\s]+?)\-\-\}', '<del>\\1</del>'])
    P.append(['\{\=\=([\S\s]+?)\=\=\}', '<mark>\\1</mark>'])
    P.append(['\{\>\>([\S\s]+?)\<\<\}', '<span class="critic comment">\\1</span>'])
    P.append(['\{\>\>\<\<\}', '<span class="critic comment"></span>'])  # empty comments
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
    parser.add_argument("-s", "--strip", help="Strip MarkdownTOC", action="store_true")
    parser.add_argument(
        "-b", "--bib", help="Bibliograpy",
        metavar='in-file', type=argparse.FileType('rt', encoding='utf-8'),
        required=False)
    parser.add_argument(
        "-i", "--input", help="input file",
        metavar='in-file', type=argparse.FileType('rt', encoding='utf-8'),
        required=True)
    parser.add_argument(
        "-o", "--output", help="output file (default is 'input'.html)",
        type=str,
        required=False)
    args = parser.parse_args()

    PDOPTS = [] # https://github.com/bebraw/pypandoc
    PDOPTS.append('--standalone')
    PDOPTS.append('--columns=10000')  # https://github.com/jgm/pandoc/issues/2574
    PDOPTS.append('--include-in-header=' + os.path.expanduser('~') + '/css/markdown.css')
    PDOPTS.append('--strip-comments') # take HTML <!-- comments -->

    if (args.bib):
        PDOPTS.append('--bibliography=' + args.bib + ' --csl ieee')

    if (args.toc and args.notoc):
        print("Use either --toc or --notoc (not both). See -h")
        sys.exit()

    if (args.toc):
        PDOPTS.append('--toc')
        PDOPTS.append('--toc-depth=5')

    if (not args.output):
        fname, fext = os.path.splitext(args.input.name)
        args.output = fname + '.html'
        exists = os.path.isfile(args.output) # 4/10/2019 - seems some html was getting appended
        if exists:
            os.remove(args.output)

    print('Processing ' + args.input.name + '...')
    in_file = args.input
    in_text = in_file.read()
    in_text = in_text.split('\n')
    in_file.close()

    # 4/25/2019
    # Add title to the page by replacing the first header with metadata character
    # this is used as title for browser tab and for internal title
    in_text[0] = in_text[0].replace("#", "%")

    out_text = preProcessMarkups(in_text)
    if (args.strip):
        out_text = stripToc(out_text)
    out_text = addAnchors(out_text)

    out_text = '\n'.join(out_text)

    # 9/22/2020
    # Want to start adding modification tag to bottom of the page
    # cmd_str = "date -d @`stat --format=%Y " +  args.input.name + "`"
    # out_text += "\n\n---\n\n``Modified: " +  os.popen(cmd_str).read() + "``"
    # 6/8/2023 - doesn't seem to be working on MinW64 - following seems to 
    # be a reasonable replacement
    p = datetime.datetime.fromtimestamp(os.path.getmtime(args.input.name))
    out_text += "\n\n---\n\n``Modified: " +  p.ctime() + "``"

    print('Creating ' + args.output + '...')
    out_html = pypandoc.convert_text(
        out_text,
        to='html5', format='md', extra_args=PDOPTS)
    out_html = re.sub('\r\n', '\n', out_html) # 202306607 - finally got rid of double spacing
    f = open(args.output, 'w', encoding='UTF-8')
    f.write(out_html)
    f.close()
