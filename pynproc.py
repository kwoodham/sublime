#!/bin/python

import pypandoc
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--notoc", help="No TOC (default)", action="store_true")
parser.add_argument("-t", "--toc", help="Include TOC", action="store_true")
parser.add_argument("-b", "--bib", help="Bibliograpy", type=str)
parser.add_argument("input", help="input file", type=str)
args = parser.parse_args()

# Check args (probably some way to do this automagically)
if (args.toc and args.notoc):
    print("Use either --toc or --notoc (not both). See -h")
    sys.exit()

cwd = os.getcwd()
i_file = cwd + os.path.basename(args.input)
o_file = i_file.replace('.md','.html')

P = []
P. append(['\[\[([-0-9A-Za-z]+)\]\]', '[\\1](\\1.html)'])

PDOPTS = ''
PDOPTS = PDOPTS + ' --from markdown+simple_tables+auto_identifiers' 
PDOPTS = PDOPTS + ' --smart --standalone'
PDOPTS = PDOPTS + ' --include-in-header=$HOME/css/markdown.css'

if (args.toc):
    PDOPTS = PDOPTS + ' --toc'

if (args.bib): 

# Form sed string - first for critic markups
SEDSTR=''
SEDSTR=$SEDSTR's/{++/<ins>/g;s/++}/<\/ins>/g'
SEDSTR=$SEDSTR';s/{--/<del>/g;s/--}/<\/del>/g'
SEDSTR=$SEDSTR';s/{~~/<del>/g;s/~>/<\/del><ins>/g;s/~~}/<\/ins>/g'
SEDSTR=$SEDSTR';s/{>>/<span class="critic comment">/g;s/<<}/<\/span>/g'
SEDSTR=$SEDSTR';s/{==/\<mark>/g;s/==}/<\/mark>/g'

# Now for "panproc" link changes
SEDSTR=$SEDSTR';s/\[\[\([-0-9A-Za-z]\{1,\}\)\(\]\]\)/[\1](.\/\1.html)/g'
SEDSTR=$SEDSTR';s/.md)/.html)/g'
SEDSTR=$SEDSTR';s/.md#/.html#/g'
SEDSTR=$SEDSTR';s/.md$/.html/g'

# Check to see if there is a need to process MarkdownTOC content
temp=$(grep "MarkdownTOC" $1)

if [ ${#temp} -gt 0 ]
    then 
		# Remove MarkdownTOC lines and store results in ".tmp" before sec/pandoc
		$HOME/.local/bin/strip_toc.py "$DIR/$TARGET".md
		sed "$SEDSTR" "$DIR/$TARGET".tmp | pandoc $PDOPTS -o "$DIR/$TARGET".html
		rm -f "$DIR/$TARGET".tmp
	else
		sed "$SEDSTR" < $1 | pandoc $PDOPTS -o "$DIR/$TARGET".html
fi

# Take out pandoc's style line that keeps code text from wrapping
sed -i '/<style type=/d' "$DIR/$TARGET".html


>>> r1 = '\[\[([a-z]+)'
>>> temp2 = re.sub(r1,r2,temp)
>>> temp2
'1]]'
>>> r2 = '\[\\1'
>>> temp2 = re.sub(r1,r2,temp)
>>> temp2
'\\[this]]'
>>> r2 = '\\1'
>>> temp2 = re.sub(r1,r2,temp)
>>> temp2
'this]]'
>>> temp2 = re.sub(r1,r2,temp)
>>> r1 = '\[\[([a-z]+)\]\]'
>>> temp2 = re.sub(r1,r2,temp)
>>> temp2
'this'
>>> r2 = '\[\\1\]'
>>> temp2 = re.sub(r1,r2,temp)
>>> temp2
'\\[this\\]'
>>> r2 = '[\\1]'
>>> temp2 = re.sub(r1,r2,temp)
>>> temp2
'[this]'
>>> r2 = '[\\1](\\1.html)'
>>> temp2 = re.sub(r1,r2,temp)
>>> temp2
'[this](this.html)'
>>>
