import sublime_plugin
import sublime

# 20171106 - added in capability to choose all (including done) and all-active (not done state).
# See corresponding way to search for inclusion in the list of states in "show_instances.py"

# 20171108 - corrected last line to pass a single element list instead of a text string if
# one item selected: self.a[index]  --> [self.a[index]]

class TaskInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.a = []
        self.a.append("All-Active")
        self.a.append("@task")
        self.a.append("@next")
        self.a.append("@working")
        self.a.append("@waiting")
        self.a.append("@done")

        # timeout fix at https://github.com/tosher/Mediawiker/blob/master/mediawiker.py
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(self.a, self.on_done), 1)

    def on_done(self, index):
        if index == -1:
            return
        print(self.a[index])
        if self.a[index] == "All-Active":
            self.a.remove("All-Active")
            self.a.remove("@done")
            self.view.run_command("show_instances", {"args": {'text': self.a}})
        else:
            self.view.run_command("show_instances", {"args": {'text': [self.a[index]]}})
