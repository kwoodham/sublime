import sublime_plugin
import sublime

# See https://www.ascii.cl/htmlcodes.htm
# 23 Oct 2017


class CleanUnicodeCommand(sublime_plugin.TextCommand):


    def run(self, edit):
        a = {}
        a[ 169] = "(C)"
        a[ 174] = "(R)"
        a[8211] = "--"
        a[8212] = "--"
        a[8216] = "'"
        a[8217] = "'"
        a[8220] = '"'
        a[8221] = '"'
        a[8226] = "-"
        a[8230] = "..."
        a[8482] = "(TM)"
        for key, value in a.items():
            locations = self.view.find_all(chr(key))
            for b in locations:
                self.view.replace(edit, b, value)
