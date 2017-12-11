import sublime_plugin
import sublime

# 20171211 - read in states via settings file - also use settings to define which states are considered
# to be active - so that only those states are displayed for "All Active"


# 20171106 - added in capability to choose all (including done) and all-active (not done state).
# See corresponding way to search for inclusion in the list of states in "show_instances.py"

# 20171108 - corrected last line to pass a single element list instead of a text string if
# one item selected: self.a[index]  --> [self.a[index]]

class TaskInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        settings = sublime.load_settings("Task.sublime-settings")
        # List of task state keywords
        keywords = settings.get('keywords')
        # List of keywords that are considered to be active (including those waiting)
        self.active = settings.get('active')

        self.a = []
        self.a.append("All-Active")
        self.a.extend(keywords)

        # timeout fix at https://github.com/tosher/Mediawiker/blob/master/mediawiker.py
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(self.a, self.on_done), 1)

    def on_done(self, index):
        if index == -1:
            return

        if self.a[index] == "All-Active":
            self.a.remove("All-Active")
            # If we are selecting all active, parse out any inactive states
            b = []
            for x in range(0, (len(self.a) - 1)):
                if self.active[x]: 
                    b.append(self.a[x])
            self.a = b
            self.view.run_command("show_instances", {"args": {'text': self.a}})
        else:
            self.view.run_command("show_instances", {"args": {'text': [self.a[index]]}})
