import sublime_plugin
import sublime
import os

# November 18, 2016
# Really basic right now: got tired of copying path using mouse from
# sidebar and forming a link in markdown using the clipboard. This shows
# a list of files in the quickview - select one and a link is created
# in the text at the cursor.

# November 18, 2016 - update - use any highlighted text as label
# November 18, 2016 - update - add in "!" prefix for image links


class FilePathCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # Read in list of image extensions
        settings = sublime.load_settings("filePath.sublime-settings")
        self.image_exts = settings.get('image_exts', [])

        # Instantiate the file reference string
        # If there is highlighted text, use it as a label
        sel = self.view.sel()[0]
        if len(self.view.substr(sel)) != 0:
            self.outStr = self.view.substr(sel)
            self.view.run_command("cut")
        else:
            self.outStr = []

        # Get a list of files in the current directory and list
        dir = os.path.dirname(self.view.file_name())
        self.a = os.listdir(dir)
        self.view.window().show_quick_panel(self.a, self.on_done)

    def on_done(self, index):

        # for the link string, use the label if given, otherwise the
        # the filename is the label
        fname = self.a[index]
        if len(self.outStr) != 0:
            self.outStr = "[" + self.outStr + "](./" + fname + ")"
        else:
            self.outStr = "[" + fname + "](./" + fname + ")"

        # Check if the file is an image file. If so, pre-pend with "!"
        if fname[fname.find("."):] in self.image_exts:
            self.outStr = "!" + self.outStr

        # Write out the string
        self.view.run_command("insert_text", {"args": {'text': self.outStr}})
