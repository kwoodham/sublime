import sublime_plugin
from User.slugify import slugify
from User.form_index import formIndexProc
import re
import os

# This just takes highlighted text, and generates a link to a slugified file named from the text.
# Based on code from CreateSubtopic
#
# 26 July 2022

class CreateTopic(sublime_plugin.TextCommand):

    def run(self, edit):

        # Generate the link text and paste into the source file
        sel = self.view.sel()[0]
        if len(self.view.substr(sel)) != 0:  # There is highlighted text - use it
            txt = self.view.substr(sel)
            file_arg = slugify(txt, "-") + ".md"
            outStr = "[" + txt + "](./" + file_arg + ")\n"
        else: 
            print("Hmmm.... nothing is highlighted")
            return
        self.view.replace(edit, sel, outStr)  # Write the link into the markdown

        # Create the full path to the new file
        wd = os.path.dirname(self.view.file_name())
        file_arg = wd.replace("\\", "/") + "/" + file_arg

        # Create the header text for the new file
        proj_arg = self.view.window().project_data()
        outStr = formIndexProc(file_arg, proj_arg)

        f = open(file_arg, 'w', encoding='utf-8')
        f.write("# " + txt + "\n\n")
        f.write(outStr)
        f.close()
