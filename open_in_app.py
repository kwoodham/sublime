import sublime_plugin
import sublime
import subprocess
import os


class OpenInAppCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = sublime.load_settings("OpenInApp.sublime-settings")
        ext_list = settings.get('ext_list', [])
        arg_list = settings.get('arg_list', [])
        app_list = settings.get('app_list', [])

        # Get the path/file (always relative to view) that
        # the cursor is in
        sel = self.view.sel()[0]
        text = self.view.substr(self.view.line(sel))
        position = self.view.rowcol(sel.begin())[1]
        lPath = text.rfind("(", 0, position)
        rPath = text.find(")", position)
        text_path = text[(lPath+1):rPath]

        # Get the absolute view path, and assemble the
        # absolute path to the file
        view_path = os.path.dirname(self.view.file_name())
        view_path = view_path.replace("\\", "/") + "/"
        abs_path = os.path.join(view_path, text_path)

        # Get the extension and see if it's one we process
        ext = os.path.splitext(text_path)[1]
        try:
            index = ext_list.index(ext)
        except:
            print("Extension: " + ext + " is not handled.")
            return

        # Launch the application with arguments and file
        try:
            subprocess.Popen([app_list[index], arg_list[index], abs_path])
        except:
            print("Oops, something bad happened.")
            return
