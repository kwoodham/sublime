import sublime_plugin


class StrikeCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        sel = self.view.sel()[0]
        text = self.view.substr(sel)
        if text[:3] == "<s>":
            text = text.replace("<s>", "")
            text = text.replace("</s>", "")
            self.view.replace(edit, sel, text)
        else:
            self.view.replace(edit, sel, "<s>" + text + "</s>")
