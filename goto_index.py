import sublime
import sublime_plugin

class GotoIndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        a = self.view.window().project_data().get('folders')
        b = a[0].get('path')
        b = b.replace("\\", "/") +  "/index.md"

        isView = self.view.window().find_open_file(b)
        if isView:
            self.view.window().focus_view(isView)
        else:
            self.view.window().open_file(b)
