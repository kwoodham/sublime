import sublime_plugin
import sublime
import subprocess
import os
import platform


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
        msg = txt[beg:end]

        try:
            subprocess.Popen([app, arg, msg])
        except:
            print("Oops, something bad happened.")
            return
