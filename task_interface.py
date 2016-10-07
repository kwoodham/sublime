import sublime_plugin
import sublime


class TaskInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.a = []
        self.a.append("@task")
        self.a.append("@done")
        self.a.append("@pend")
        self.a.append("@push")
        # timeout fix at https://github.com/tosher/Mediawiker/blob/master/mediawiker.py
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(self.a, self.on_done), 1)

    def on_done(self, index):
        if index == -1:
            return
        print(self.a[index])
        self.view.run_command("show_instances", {"args": {'text': self.a[index]}})
