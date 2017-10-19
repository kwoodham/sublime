import sublime
import sublime_plugin
import sublime
import datetime

# 2017-10-19  
# Assumes single year journal page generated by new_year_single.py
# Clean up code - move function out from under class definition

class GotoTodaySingleCommand(sublime_plugin.TextCommand):
    newView = () # Global defined for pass to event handler if needed

    def run(self, edit):
        # root_dir is root of journal WRT project root. Assumes year
        # folders under root_dir
        settings = sublime.load_settings("GotoToday.sublime-settings")
        root_dir = settings.get('root_dir', "./")


        # Get the year as a string
        outStr = datetime.date.today().strftime("%Y")
       
        # Get project path and assemble /project/root_dir/year/year.md
        a = self.view.window().project_data().get('folders')
        b = a[0]['path']
        b = b.replace("\\", "/") + "/"
        outStr = b + root_dir + outStr+ "/" + outStr + ".md"

        # If this is a current view switch and center, otherwise load
        # the file and have the event handler center the view when loaded
        isView = self.view.window().find_open_file(outStr)
        if isView:
            self.view.window().focus_view(isView)
            center_today(isView)
        else:
            GotoTodaySingleCommand.newView = self.view.window().open_file(outStr)


class EventListener(sublime_plugin.EventListener):

    def on_load_async(self, view):
        center_today(GotoTodaySingleCommand.newView)


def center_today(view):
    a = "### " + datetime.date.today().strftime("%a %b %d")
    b = view.find(a, 0)
    view.show_at_center(b)