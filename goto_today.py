import sublime_plugin
import sublime
import datetime


class GotoTodayCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # root_dir is root of journal WRT project root. Assumes year
        # folders under root_dir
        settings = sublime.load_settings("GotoToday.sublime-settings")
        root_dir = settings.get('root_dir', "./")

        # Process data and offset. ( weekday is offset from Monday)
        a = datetime.date.today()
        b = datetime.date.fromordinal(a.toordinal()-a.weekday())
        c = a.year
        outStr = b.strftime("%Y%m%d") + ".md"

        # Get project path and assemble /project/root_dir/year/file.md
        a = self.view.window().project_data().get('folders')
        b = a[0]['path']
        b = b.replace("\\", "/") + "/"
        outStr = b + root_dir + str(c) + "/" + outStr

        # If this is a current view switch and center, otherwise load
        # the file and give a modest timeout before centering the view
        isView = self.view.window().find_open_file(outStr)
        if isView:
            self.view.window().focus_view(isView)
            GotoTodayCommand.center_today(isView)
        else:
            newView = self.view.window().open_file(outStr)
            sublime.set_timeout(lambda: GotoTodayCommand.center_today(newView), 500)
            

    def center_today(view):
        a = "## " + datetime.date.today().strftime("%A, %B %d, %Y")
        b = view.find(a, 0)
        view.show_at_center(b)
