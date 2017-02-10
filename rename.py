import sys
import os
import datetime
from slugify import slugify

fileName, fileExt = os.path.splitext(str(sys.argv[1]))
d = datetime.datetime.fromtimestamp(os.path.getctime(str(sys.argv[1])))
leadStr = "{0:0>4}".format(d.year)
leadStr = leadStr + "{0:0>2}".format(d.month)
leadStr = leadStr + "{0:0>2}".format(d.day)
leadStr = leadStr + "{0:0>2}".format(d.hour)
leadStr = leadStr + "{0:0>2}".format(d.minute)
fileStr = leadStr + "_" + slugify(fileName, "-") + fileExt

sys.stdout.write("Rename " + sys.argv[1] + " to " + fileStr + "? [Y/n]")
choice = input().lower()
if choice == '' or choice == 'y':
    os.rename(sys.argv[1], fileStr)
