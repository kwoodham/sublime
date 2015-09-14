import sublime_plugin


class TaskToggleCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # get the current line
        sel = self.view.sel()[0]   # cursor region
        lin = self.view.line(sel)  # line region
        text = self.view.substr(lin)

        if text[0] != "@":
            text_out = "@task `" + text + "`"
            self.view.replace(edit, lin, text_out)
        else:
            if text[:5] == "@task":
                self.view.replace(edit, lin, text.replace("@task", "@pend"))
                return
            elif text[:5] == "@pend":
                text = text.replace("@pend ", "@done <s>") + "</s>"
                self.view.replace(edit, lin, text)
                return
            elif text[:5] == "@done":
                text = text.replace("@done <s>", "@task ")
                self.view.replace(edit, lin, text.replace("</s>", ""))
                return
            else:
                print("I don't know how to transition from this task state")
