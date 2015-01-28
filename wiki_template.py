import sublime_plugin
import datetime
import os


class WikiTemplateCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file_name = os.path.basename(self.view.file_name())
        a = file_name[:file_name.find(".")]  # Get the string without the ".md"
        b = datetime.date(int(a[:4]), int(a[4:6]), int(a[6:]))
        c = datetime.timedelta(days=1)  # One day time increment
        sel = self.view.sel()  # This returns a RegionSet (only one region)
        for s in sel:
            outStr = "# Week of " + a + "\n\n"
            outStr = outStr + "[[" + str(b.year) + "]]\n\n"
            outStr = outStr + "## Goals/Tasks\n\n\n"
            end = s.b + self.view.insert(edit, s.b, outStr)
            for x in range(0, 5):  # 0 = Monday, 6 = Sunday
                outStr = "## " + b.strftime("%A, %B %d, %Y")+"\n\n\n"
                end = end + self.view.insert(edit, end, outStr)
                b = b + c  # Increment date by one day
