#!/usr/bin/python3

import subprocess
import sys
import re

P = []
P.append(['<lb type="x-begin-paragraph"/>', ''])
P.append(['<lb type="x-end-paragraph"/>', '\\'])
P.append(['<q marker="">',''])
P.append(['<q>',''])
P.append(['<milestone marker="&#8220;" type="cQuote"/>', '"'])
P.append(['<milestone marker="&#8221;" type="cQuote"/>', '"\\'])
P.append(['<q level="1" marker="&#8220;"/>', '"'])
P.append(['<q level="1" marker="&#8221;"/>', '"\\'])
P.append(['<q level="2" marker="&#8216;"/>', "'"])
P.append(['<q level="2" marker="&#8217;"/>', "'"])
P.append(['(ESV)', ''])

re_str = '\s[es]ID\=\"[0-9.]+\"'

refs = ' '.join((sys.argv[1:]))
argd = "-b ESV -e HTML -k "
cmds = "diatheke " + argd + refs 

text = subprocess.Popen(cmds, shell=True, stdout=subprocess.PIPE).stdout.read()
text = text.decode("utf-8")
f = text.split('\n')

# f = open('temp.txt', 'r')
# f = f.read()
# f = f.split('\n')


# Do markup replacements and store results in f1
f1 = []
for line in f:
    line = re.sub(re_str, '', line)
    for i in range(0, len(P)):
        line = line.replace(P[i][0], P[i][1])
    f1.append(line)

# Only want verse numbers if book and chapter haven't change
# from the previous line
f2 = []
book_chap = ''
for line in f1:
    if line[0:line.find(':')] == book_chap:
        line = line.replace(line[0:(line.find(':')+1)], '')
    else:
        book_chap = line[0:line.find(':')]
    f2.append(line)

# Want consecutive verses in paragraphs if no hard-coded 
# breaks are at the end of the verse
f3 = []
new_para = ''
for line in f2:
    if line.find('\\') > -1:
        line = line.replace('\\','')
        line = line.strip()
        new_para = new_para + ' ' + line
        new_para = new_para.lstrip()
        f3.append(new_para)
        f3.append('')
        new_para = ''
        last_write = int(1)
    else:
        line = line.lstrip()
        new_para = new_para + ' ' + line
        last_write = int(0)
if not last_write:
    new_para = new_para.lstrip()
    f3.append(new_para)
    f3.append('')

for line in f3:
    print(line)