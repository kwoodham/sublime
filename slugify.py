#!/bin/python

import unicodedata
import re
import sys
import os

# From markdown utilities, with the addition that periods are allowed
# in the header per the pandoc definition. Note that for Sublime.
# this has to be inported using:
#
# from User.slugify import slugify
#
# 2016-03-21 took out the "+" in the last re so that "text - text" would
# be rendered  "text---text" in agreement with how pandoc generates the
# html anchors.
#
# 2019-09-21 os.path.splitext was spliting at the first occurance of "." so
# it would leave everything after a "." in the filenane un-slugged and
# append it back onto what was slugged - thinking the whole string was the
# extension. Best thing to do would be just not break out the extension
# for files (I generally use lower-case extensions anyhow, and I can't
# think of an extension that matters).
# 
# Also added "." back into re so that string would match what MarkdownTOC 
# generates (with "." removed from matching pattern) as well as pandoc.



def slugify(value, separator):
    """ Slugify a string, to make it URL friendly. """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub('[^\w_ .-]', '', value.decode('ascii')).strip().lower()
    return re.sub('[%s\s]' % separator, separator, value)

if __name__ == '__main__':
    # 2019-09-21 fileName, fileExt = os.path.splitext(str(sys.argv[1]))
    # 2019-09-21 fileStr = slugify(fileName, "-") + fileExt
    fileStr = slugify(str(sys.argv[1]), "-")
    sys.stdout.write("Rename " + sys.argv[1] + " to " + fileStr + "? [Y/n]")
    choice = input().lower()
    if choice == '' or choice == 'y':
        os.rename(sys.argv[1], fileStr)
