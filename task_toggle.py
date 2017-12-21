import sublime
import sublime_plugin

# 11 Dec 2017 - Old - Use task_toggle2

# 06 Dec 2017 - started using "######" (heading 6) so that I can generate
# anchors to tasks.

# 13 Nov 2017 - add in check for empty line, include erasing of all 
# markup as wrap-around state, and cleanup of logic.


class TaskToggleCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        settings = sublime.load_settings("Task.sublime-settings")
        lead = settings.get('lead')
        offset = len(lead)

        # get the current line
        sel = self.view.sel()[0]   # cursor region
        lin = self.view.line(sel)  # line region
        text = self.view.substr(lin)
        keywords = ["TASK", "NEXT", "WORK", "WAIT", "DONE", "KILL"]

        if text == '':
            print("Error - no text found on this line")
        else:
            if text[offset:offset+4] not in keywords:
                text_out = lead + "TASK `" + text + "`"
                self.view.replace(edit, lin, text_out)
            elif text[offset:offset+4] == "TASK":
                self.view.replace(edit, lin, text.replace("TASK", "NEXT"))
                return
            elif text[offset:offset+4] == "NEXT":
                self.view.replace(edit, lin, text.replace("NEXT", "WORK"))
                return
            elif text[offset:offset+4] == "WORK":
                self.view.replace(edit, lin, text.replace("WORK", "WAIT"))
                return
            elif text[offset:offset+4] == "WAIT":
                text = text.replace("WAIT ", "DONE <s>") + "</s>"
                self.view.replace(edit, lin, text)
                return
            elif text[offset:offset+4] == "DONE":
                text = text.replace("DONE ", "KILL ")
                self.view.replace(edit, lin, text)
                return
            elif text[offset:offset+4] == "KILL":
                text = text.replace(lead + "KILL <s>`", "")
                self.view.replace(edit, lin, text.replace("`</s>", ""))
                return
            else:
                print("I don't know how to transition from this task state")
