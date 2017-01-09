# Convert message export done in CodeTwo Outlook export into Markdown "quote" format
# 12/19/2016 - use "alias cvsit='py -3 /c/Users/kpwoodha/.local/bin/csv_proc.py'" or
# equivalent to use from bash

import sys
import os
import csv

fileName, fileExt = os.path.splitext(str(sys.argv[1]))
if (fileExt != '.csv'):
    print("Not a csv extension!")
    sys.exit()

outfile = fileName + ".md"

b = []
with open(sys.argv[1], newline='') as csvfile:
    a = csv.reader(csvfile, delimiter='\t', quotechar='"')
    for row in a:
        b.append(row)
csvfile.close()

# Print out header (make sure that these strings match what is used in CodeTwo export,
# but they don't have to be in this order)
with open(outfile, 'w', encoding='utf-8') as c:
    c.write("> " + b[0][b[0].index('From')] + ":    " + b[1][b[0].index('From')])
    c.write("> " + b[0][b[0].index('To')] + ":      " + b[1][b[0].index('To')])
    c.write("> " + b[0][b[0].index('Date')] + ":    " + b[1][b[0].index('Date')])
    c.write("> " + b[0][b[0].index('Subject')] + ": " + b[1][b[0].index('Subject')])

    # Get rid of extra annoying line feeds in the body, and print it out
    b[1][b[0].index('Body')] = b[1][b[0].index('Body')].replace('\r\n\r\n \r\n\r\n', '\n>\n> ')
    b[1][b[0].index('Body')] = b[1][b[0].index('Body')].replace('\r\n\r\n', '\n> ')
    c.write(">\n> " + b[1][b[0].index('Body')])
c.close()
