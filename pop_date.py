import sublime_plugin
import time

# See: https://sublimetext.com/forum/viewtopic.php?f=6&p=45530
# re method for not having to try to pass edit object to on_done.
# (Solution: create another text edit class, and invoke it
# within "on_done")


class PopDateCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        PopDateCommand.globalEdit = edit
        self.a = []
        self.a.append(time.strftime("%Y%m%d"))
        self.a.append(time.strftime("%d %b %Y"))
        self.a.append(time.strftime("%B %d, %Y"))
        self.a.append(time.strftime("%A, %B %d, %Y"))
        self.a.append(time.strftime("%I:%M %p"))
        self.a.append(time.strftime("%d %b %Y, %I:%M %p"))
        self.a.append(time.strftime("%A, %B %d, %Y %I:%M %p"))
        self.view.show_popup_menu(self.a, self.on_done)

    def on_done(self, index):
        if index == -1:
            return
        self.view.run_command("insert_text", {"args": {'text': self.a[index]}})


class InsertText(sublime_plugin.TextCommand):

    def run(self, edit, args):

        sel = self.view.sel()[0]
        self.view.insert(edit, sel.a, args['text'])
