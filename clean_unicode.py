import sublime_plugin
import sublime

# See https://www.ascii.cl/htmlcodes.htm
# 23 Oct 2017
# Revised 29 June 2020


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
            # 20200626 do this one at a time, as location of next instance shifts if 
            # the previous substitution was multi-character (such as "(C)").
            loc = self.view.find(chr(key), 0)
            count = 0
            while loc:
                loc = self.view.find(chr(key), 0)
                if loc: 
                    self.view.replace(edit, loc, value)
                    count += 1
            print("processing " + chr(key) + ": found " + str(count) + " instances.")
