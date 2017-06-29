import sys
import os
import re
from slugify import slugify

fileName, fileExt = os.path.splitext(str(sys.argv[1]))
fileStr = slugify(fileName, "-") + fileExt

# Strip out the repeated "-" that are formed sometimes by slugify
regex = r"[-]+"
subst = "-"
fileStr = re.sub(regex, subst, fileStr, 0)

sys.stdout.write("Rename " + sys.argv[1] + " to " + fileStr + "? [Y/n]")
choice = input().lower()
if choice == '' or choice == 'y':
    os.rename(sys.argv[1], fileStr)
