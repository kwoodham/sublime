import datetime
import sublime_plugin

# https://stackoverflow.com/questions/11879481/can-i-add-date-time-for-sublime-snippet


class AddDate1Command(sublime_plugin.TextCommand):
    def run(self, edit): # '16 May 2019'
        self.view.run_command("insert_snippet", {"contents": "%s" % datetime.date.today().strftime("%Y%m%d")})

class AddDate2Command(sublime_plugin.TextCommand):
    def run(self, edit): # '16 May Thu'
        self.view.run_command("insert_snippet", {"contents": "%s" % datetime.date.today().strftime("%d %b %a")})

class AddTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet", {"contents": "%s" % datetime.datetime.now().strftime("%H:%M")})
