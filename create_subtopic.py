import sublime_plugin
from User.slugify import slugify

# This just takes a header string, and generates a link to the index in the associated
# namespace (which is assumed to be a subfolder named as a slugification of the header)


class CreateSubtopic(sublime_plugin.TextCommand):

    def run(self, edit):

        sel = self.view.sel()[0]
        text_in = self.view.substr(sel)
        text_out = text_in + "\n"
        text_out = text_out + "[" + text_in + "](./" + slugify(text_in, "-") + "/index.md)\n"
        self.view.replace(edit, sel, text_out)
