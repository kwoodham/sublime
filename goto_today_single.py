import sublime
import sublime_plugin
import datetime
import os

# 2017-12-21
# If there is a something like "/projects/larc/2016-fueleap", then I want
# the journal to be in fueleap. Add in "metaproj" list in the settings to
# account for these.

# So directory structure is:

# sublime project folder/projects/(metaproject)/project/year/year.md
# if metaproject is in "subproj" list in settings

# 2017-12-21
# If there is a directory: /projects/subprojects/year/year.md and the
# subproj switch is set, the entry will go in the subproject's journal
# instead of the top-level journal.

# Also hard-coding structure as above (doing away with root journal
# designation in settings.

# 2017-12-05
# New approach - had so many blank entries - particularly in project-
# specific journals - so now this creates a day header if one isn't there
# for the current day. So I plan to use this with an otherwise empty file
# so there won't be headers for empty days.

# 2017-10-19
# Assumes single year journal page generated by new_year_single.py
# Clean up code - move function out from under class definition


class GotoTodaySingleCommand(sublime_plugin.TextCommand):
    newView = ()  # Global defined for pass to event handler if needed

    def run(self, edit):
        # Get "subprojects" switch
        settings = sublime.load_settings("GotoToday.sublime-settings")
        subproj = settings.get('subproj', 0)
        metaproj = settings.get('metaproj', [])

        # Get the year as a string
        outStr = datetime.date.today().strftime("%Y")

        # Get project path:
        a = self.view.window().extract_variables()['folder']

        # Check for existence of valid subproject journal file if the subproj
        # switch is set, otherwise point to top-level journal
        # Process the "metaproject" level if the path is identified as a
        # metaproject per the settings.
        if subproj:
            b = self.view.window().extract_variables()['file_path']
            b = os.path.relpath(b, a)
            b = b.split("\\")
            if b[0] == 'projects':
                subproj_path = a + "\\" + b[0] + "\\" + b[1] + "\\"
                if b[1] in metaproj:
                    subproj_path = subproj_path + b[2] + "\\"
                subproj_path = subproj_path + outStr + "\\" + outStr + ".md"
                if os.path.isfile(subproj_path):
                    a = subproj_path
                else:  # subproject journal doesn't exist
                    a = a + "\\" + outStr + "\\" + outStr + ".md"
            else:  # the top-level relative folder is not "projects"
                a = a + "\\" + outStr + "\\" + outStr + ".md"
        else:  # subproj switch is not set (use top level journal)
            a = a + "\\" + outStr + "\\" + outStr + ".md"

        # Open the file if need be and switch the view to it, then
        # use the CenterToday class to center today's entries in the
        # window - delay is set to make sure that ST3 has time to load the
        # file and focus the view
        isView = self.view.window().find_open_file(a)
        if isView:
            newView = isView
        else:
            newView = self.view.window().open_file(a)
        self.view.window().focus_view(newView)
        sublime.set_timeout(lambda: newView.run_command('center_today'), 500)


class CenterToday(sublime_plugin.TextCommand):

    def run(self, edit):
        a = "## " + datetime.date.today().strftime("%a %b %d")
        b = self.view.find(a, 0)
        if (b.a == -1) & (b.b == -1):
            sel_b = self.view.size()
            end = sel_b + self.view.insert(edit, sel_b, "\n\n" + a + "\n\n")
            self.view.show_at_center(end)
        else:
            self.view.show_at_center(b)  # can be point or region
