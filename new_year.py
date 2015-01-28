import sublime_plugin
import sublime
import datetime


class NewYearCommand(sublime_plugin.TextCommand):

    def on_done(self, index):
        if index == -1:
            return

        self.view.run_command("generate_year_wiki",
            {"args": {'text': self.list[index]}})

    def run(self, edit):
        self.year = datetime.datetime.now().year
        self.list = [(self.year+a) for a in range(-4, 5)]
        self.list = ['%04d' % a for a in self.list]
        self.view.window().show_quick_panel(self.list, self.on_done)


class GenerateYearWiki(sublime_plugin.TextCommand):

    def run(self, edit, args):
        # Initialize
        year = int(args['text'])
        week = datetime.timedelta(days=7)
        monthName = 'Start'
        isoWeeks = int(0)
        endDate = int(31)

        # Find the last week number of the year (not rolled over)
        # Rationale: some of December can be in Week 1 of following
        # year - I want the week number of the last date before the
        # days roll over into the next week number.
        while isoWeeks < 50:
            isoWeeks = (datetime.date(year, 12, endDate)).isocalendar()[1]
            endDate = endDate - 1

        # Print the header
        outStr = '# Calendar Year: ' + '%04d' % year + '\n'
        end = self.view.insert(edit, 0, outStr)

        # Find the first Sunday (0=Mon, 6=Sun) of the year
        jan1 = datetime.date(year, int(1), int(1))
        offset = datetime.timedelta(days=(int(0) - int(jan1.weekday())))
        monday = jan1 + offset

        # Print out ISO week # and a file link for each week.
        # Put a blank line and month header before each month
        for i in range(0, isoWeeks):
            if monday.strftime("%B") != monthName:
                monthName = monday.strftime("%B")
                outStr = '\n## ' + monthName + ':\n'
                end = end + self.view.insert(edit, end, outStr)

            outStr = '%02d' % monday.isocalendar()[1]
            outStr = outStr + ' [['
            outStr = outStr + monday.strftime("%Y%m%d")
            outStr = outStr + ']]\\\n'
            end = end + self.view.insert(edit, end, outStr)
            monday = monday + week

        # Take the "\" break off of the last week of the month
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)
        content = content.replace('\\\n\n', '\n\n')
        self.view.replace(edit, region, content)
