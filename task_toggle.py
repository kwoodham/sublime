import sublime_plugin
import sublime
import subprocess
import os


class TaskToggleCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # get the current line
        sel = self.view.sel()[0]  # cursor region
        lin = self.view.line(sel) # line region
        text = self.view.substr(lin)

        if text[0] != "@":
            text_out = "@task `" + text + "`"
            self.view.replace(edit,lin,text_out)
        else:
            if text[:5] == "@task":
                self.view.replace(edit,lin,text.replace("@task","@pend"))
                return
            elif text[:5] == "@pend":
                text = text.replace("@pend ","@done <s>") + "</s>"
                self.view.replace(edit,lin,text)
                return
            elif text[:5] == "@done":
                text = text.replace("@done <s>","@task ")
                text = text.replace("</s>","")
                self.view.replace(edit,lin,text)
                return
