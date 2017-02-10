import sys
import os
from slugify import slugify

fileName, fileExt = os.path.splitext(str(sys.argv[1]))
fileStr = slugify(fileName, "-") + fileExt

sys.stdout.write("Rename " + sys.argv[1] + " to " + fileStr + "? [Y/n]")
choice = input().lower()
if choice == '' or choice == 'y':
    os.rename(sys.argv[1], fileStr)
