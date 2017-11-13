import sublime_plugin

# 13 Nov 2017 - update - add in check for empty line, include erasing of all 
# markup as wrap-around state, and cleanup of logic.


class TaskToggleCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # get the current line
        sel = self.view.sel()[0]   # cursor region
        lin = self.view.line(sel)  # line region
        text = self.view.substr(lin)

        if text == '':
            print("Error - no text found on this line")
        else:
            if text[0] != "@":
                text_out = "@task `" + text + "`"
                self.view.replace(edit, lin, text_out)
            elif text[:5] == "@task":
                self.view.replace(edit, lin, text.replace("@task", "@next"))
                return
            elif text[:5] == "@next":
                self.view.replace(edit, lin, text.replace("@next", "@working"))
                return
            elif text[:8] == "@working":
                self.view.replace(edit, lin, text.replace("@working", "@waiting"))
                return
            elif text[:8] == "@waiting":
                text = text.replace("@waiting ", "@done <s>") + "</s>"
                self.view.replace(edit, lin, text)
                return
            elif text[:5] == "@done":
                text = text.replace("@done ", "@deleted ")
                self.view.replace(edit, lin, text)
                return
            elif text[:8] == "@deleted":
                text = text.replace("@deleted <s>`", "")
                self.view.replace(edit, lin, text.replace("`</s>", ""))
                return
            else:
                print("I don't know how to transition from this task state")
