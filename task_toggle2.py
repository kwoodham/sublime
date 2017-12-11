import sublime
import sublime_plugin

# 08 Dec 2017 - use panel to select the keyword - don't have to follow serial state changes
# this version also applies formating to the states per the settings.

# 06 Dec 2017 - started using a "lead" (currently, heading 6) so that I can generate
# anchors to tasks.

# 13 Nov 2017 - add in check for empty line, include erasing of all 
# markup as wrap-around state, and cleanup of logic.


class TaskToggle2Command(sublime_plugin.TextCommand):

    def on_done(self, index):
        if index == -1:
            return

        # get the current line text
        sel = self.view.sel()[0]   # cursor region
        lin = self.view.line(sel)  # line region
        line_txt = self.view.substr(self.view.line(sel))


        # First case - "none": removing any task markings if there, otherwise return
        if self.keywords[index] == "none":
            if line_txt[:len(self.lead)] == self.lead:
                txt = line_txt.split("`",3)[1].rstrip()
            else:
                return

        # second case - apply keyword and marking if it's a new task, or change if old       
        else:
            if line_txt[:len(self.lead)] == self.lead:
                task_txt = line_txt.split("`",3)[1].rstrip()
            else: 
                task_txt = line_txt     
            txt = self.lead + self.keywords[index] + " " + self.formats[index][0] + "`"
            txt = txt + task_txt + "`" + self.formats[index][1]
            
        # Apply the changes to the line
        self.view.run_command( "format_task", {"args": {'text': txt}})


    def run(self, edit):

        settings = sublime.load_settings("Task.sublime-settings")
        self.lead = settings.get('lead')
        self.keywords = settings.get('keywords')
        self.keywords.extend(['none']) # Add in option to clear task formatting
        self.formats = settings.get('formats')

        self.view.window().show_quick_panel(self.keywords, self.on_done, 1)


class FormatTask(sublime_plugin.TextCommand):

    def run(self, edit, args):
        self.view.replace(edit, self.view.line(self.view.sel()[0]), args['text'])