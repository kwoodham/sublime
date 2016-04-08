import sublime_plugin
from User.slugify import slugify
import re
import os

# This just takes a header string, or hihglighted text, and generates a link to the index
# in the associated namespace (which is assumed to be a subfolder named as a slugification
# of the header or highlighted text).
#
# 30 Mar 2016 - update: assumes cursor at the end of the line (don't have to highlight
# the heading text).
#
# 30 Mar 2016 - update: if namespace subdirectory doesn't exist, create it. If index file
# doesn't exist, create it with the top level heading.
#
# 08 Apr 2016 - update: add in sigutation where text could be highlighted and it would be
# used to generate the namespace.

class CreateSubtopic(sublime_plugin.TextCommand):

    def run(self, edit):

        sel = self.view.sel()[0]
        if len(self.view.substr(sel)) != 0:  # There is highlighted text - use it
            txt = self.view.substr(sel)
            outStr = "[" + txt + "](./" + slugify(txt, "-") + "/index.md)\n"
        else:                                # Otherwise assume cursor is at end of header
            lin = self.view.line(sel)
            txt = self.view.substr(lin).split(" ")
            ans = (True if re.search('[#]+', txt[0]) else False)   # Is this a header?
            if ans:
                txt = " ".join(txt[1:])  # Everything but the leading header chars
                outStr = "\n[" + txt + "](./" + slugify(txt, "-") + "/index.md)\n"
            else:
                print("Hmmm.... this doesn't appear to be a heading, and nothing is highlighted")
                return
        self.view.replace(edit, sel, outStr)  # Write the link into the markdown

        # Generate the namespace folder (if needed) and create the index file
        wd = os.path.dirname(self.view.file_name())
        wd = wd.replace("\\", "/") + "/" + slugify(txt, "-")
        if not os.path.exists(wd):
            os.makedirs(wd)
        if not os.path.exists(wd + "/index.md"):
            f = open(wd + "/index.md", 'w', encoding='utf-8')
            f.write("# " + txt + "\n")
            f.close()
