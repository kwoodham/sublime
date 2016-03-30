import sublime_plugin
from User.slugify import slugify
import re

# This just takes a header string, and generates a link to the index in the associated
# namespace (which is assumed to be a subfolder named as a slugification of the header)
# 30 Mar 2016 - update: assumes cursor at the end of the line (don't have to highlight
# the heading text).


class CreateSubtopic(sublime_plugin.TextCommand):

    def run(self, edit):

        sel = self.view.sel()[0]
        lin = self.view.line(sel)
        txt = self.view.substr(lin).split(" ")
        ans = (True if re.search('[#]+', txt[0]) else False)   # Is this a header?
        if ans:
            heading = " ".join(txt[1:])  # Everything but the leading header chars
            outStr = "\n[" + heading + "](./" + slugify(heading, "-") + "/index.md)\n"
            self.view.insert(edit, sel.b, outStr)
        else:
            print("Hmmm.... this doesn't appear to be a heading.")
