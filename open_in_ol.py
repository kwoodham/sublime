import sublime_plugin
import sublime
import subprocess

# 07 Nov 2017 if the GUID is in a link such as:
# ...
# [message][msg1] ...
# ...
# [msg1]: outlook:00000000AD9D40BD8340CA44A8285C20FE5F08B744322100
# ...
# then there is no closing ")" - in which case I am assuming that the link
# extends to the end of the string.

class OpenInOlCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        app =  "C:\\Program Files (x86)\\Microsoft Office\\Office16\\OUTLOOK.EXE"
        arg = "/select"

        # Get the "outlook:ID" string - assume there's only one on the line
        # note that there may be other "()" pairs in the message header, so we
        # want the next ")" after "outlook:" to find the end of the ID
        sel = self.view.sel()[0]
        txt = self.view.substr(self.view.line(sel))
        beg = txt.find("outlook:")
        end = txt.find(")", beg)
        if end == -1:
            msg = txt[beg:]
        else:
            msg = txt[beg:end]

        try:
            subprocess.Popen([app, arg, msg])
        except:
            print("Oops, something bad happened.")
            return
