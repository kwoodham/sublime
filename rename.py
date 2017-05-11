import sys
import os
import datetime
from slugify import slugify
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--hour", help="add hour to string base", action="store_true")
parser.add_argument("--minute", help="add minutes to string base", action="store_true")
parser.add_argument("filename", help="name of file to rename", type=str)
args = parser.parse_args()

fileName, fileExt = os.path.splitext(args.filename)
d = datetime.datetime.fromtimestamp(os.path.getctime(str(sys.argv[1])))
leadStr = "{0:0>4}".format(d.year)
leadStr = leadStr + "{0:0>2}".format(d.month)
leadStr = leadStr + "{0:0>2}".format(d.day)
if args.hour:
    leadStr = leadStr + "{0:0>2}".format(d.hour)
if args.minute:
    leadStr = leadStr + "{0:0>2}".format(d.minute)
fileStr = leadStr + "-" + slugify(fileName, "-") + fileExt

# Strip out the repeated "-" that are formed sometimes by slugify
regex = r"[-]+"
subst = "-"
fileStr = re.sub(regex, subst, fileStr, 0)

sys.stdout.write("Rename " + sys.argv[1] + " to " + fileStr + "? [Y/n]")
choice = input().lower()
if choice == '' or choice == 'y':
    os.rename(sys.argv[1], fileStr)
