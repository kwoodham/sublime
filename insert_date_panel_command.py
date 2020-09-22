import sublime_plugin
import datetime

class InsertDatePanelCommand(sublime_plugin.TextCommand):

    def on_done(self, index):

        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return

        # if user picks from list, return the correct entry
        self.view.run_command(
            "insert_my_text", {"args":
            {'text': self.list[index]}})

    def run(self, edit):

    # this will populate the quick_panel with 4 date formats
        d1 = str(datetime.datetime.now())
        d2 = str(datetime.date.today())

        d3 = datetime.date.today().strftime("%d %B %Y (%A)") + \
            ' @ ' + datetime.datetime.now().strftime("%H:%M")

        d4 = datetime.date.today().strftime("%A, %d-%B-%Y") + \
            datetime.datetime.now().strftime(" %I:%M %p")

        self.list = [d1, d2, d3, d4]

        # show_quick_panel(items, on_done, <flags>, <default_index>)
        # ref: http://www.sublimetext.com/forum/viewtopic.php?f=4&t=7139
        # take the list, and place it in a quick_panel, make 3rd item
        # default pick

        self.view.window().show_quick_panel(self.list, self.on_done, 1, 2)


class InsertMyText(sublime_plugin.TextCommand):

    def run(self, edit, args):

        # add this to insert at current cursor position
        # http://www.sublimetext.com/forum/viewtopic.php?f=6&t=11509

        self.view.insert(edit, self.view.sel()[0].begin(), args['text'])