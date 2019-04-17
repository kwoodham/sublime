import datetime
import sublime_plugin

# https://stackoverflow.com/questions/11879481/can-i-add-date-time-for-sublime-snippet


class AddDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet", {"contents": "%s" % datetime.date.today().strftime("%d %b %Y")})


class AddTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet", {"contents": "%s" % datetime.datetime.now().strftime("%H:%M")})
