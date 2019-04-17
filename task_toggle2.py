import sublime
import sublime_plugin
import shutil
import tempfile
import os
import time

# 07 Mar 2019 use a project todo list if it exists; otherwise use the 
# default from the settings file.

# 04 Feb 2019 if task is killed, mark it as completed and apply the "kill"
# date to the task. Can tell differenced between completed and killed
# tasks by the s: flag in the archive - thought it was valuable to record
# the kill date and have the task marked as completed for archival purposes

# 04 Jan 2018 if task is placed in "end_state" (i.e. "DONE"), the current
# date is pre-pended in the todo.txt file, and the state is locked in ST.
# If the task is placed in the "del_state" (i.e. "KILL"), the state is
# locked and the task is deleted from the todo.txt file.

# Note: disable auto-purge of todo.txt if you want the done tasks to be
# listed in the kanban columns

# 22 Dec 2017 if there is an anchor assigned to the task, do not delete
# it when the stage changes

# 08 Dec 2017 - use panel to select the keyword - don't have to follow
# serial state changes. this version also applies formating to the states
# per the settings.

# 06 Dec 2017 - started using a "lead" (currently, heading 6) so that
# I can generate anchors to tasks.

# 13 Nov 2017 - add in check for empty line, include erasing of all
# markup as wrap-around state, and cleanup of logic.


class TaskToggle2Command(sublime_plugin.TextCommand):

    def on_done(self, index):
        if index == -1:
            return

        # get the current line text and a placeholder anchor text
        sel = self.view.sel()[0]   # cursor region
        line_txt = self.view.substr(self.view.line(sel))
        anch_txt = ""

        # if it looks like this has an anchor (because it has a "{"), parse the
        # line into task text and anchor.  If it has more than two parts to the
        # parse, then punt...
        if "{" in line_txt:
            line_parts = line_txt.split("{")
            if not len(line_parts) == 2:
                print("Don't know how to parse this line\n")
                return
            else:  # line contains only an anchor at the end
                line_txt = line_parts[0]
                anch_txt = " {" + line_parts[1]  # rstrip used below; need a space

        # Now work on just the task string:

        # check to see that we aren't working with a completed task:
        done_task_lead = self.lead + self.end_state  # "lead" has a built-in space
        if line_txt[:len(done_task_lead)] == done_task_lead:
            print("Cannot change state of a task marked " + self.end_state)
            print("as it likely has a completed data recorded in the todo.txt task file.\n")
            return

        # check to see that we aren't working with a deleted task:
        del_task_lead = self.lead + self.del_state  # "lead" has a built-in space
        if line_txt[:len(del_task_lead)] == del_task_lead:
            print("Cannot change state of a task marked " + self.del_state)
            print("as it has likely been deleted from the todo.txt task file.\n")
            return

        # next case - "none": removing any task markings if there, otherwise return
        if self.keywords[index] == "none":
            if line_txt[:len(self.lead)] == self.lead:
                task_txt = line_txt.split("`", 3)[1].rstrip()
                txt = task_txt
            else:
                return

        else:  # otherwise apply keyword
            if line_txt[:len(self.lead)] == self.lead:
                task_txt = line_txt.split("`", 3)[1].rstrip()
            else:
                task_txt = line_txt
            txt = self.lead + self.keywords[index] + " " + self.formats[index][0] + "`"
            if self.keywords[index] == self.end_state:
                txt = txt + time.strftime("%Y-%m-%d") + " "
            txt = txt + task_txt + "`" + self.formats[index][1]

        # Add back in the anchor (anch_txt is empty if there isn't one)
        txt = txt + anch_txt

        # Apply the changes to the line
        self.view.run_command("format_task", {"args": {'text': txt}})

        # write the task back out to the todo file.  First we get a local copy
        # of either the project todo list (if it exists) or the default todo list
        # from the settings file
        a = self.view.window().project_data().get('folders')
        b = a[0].get('path') + "\\todo\\"
        if os.path.isdir(b):
            todo_path = b + "todo.txt"
        else:
            settings = sublime.load_settings("TodoInterface.sublime-settings")
            todo_path = settings.get('todo_path', True)

        f = open(todo_path, 'r')
        s = f.read()
        f.close()
        lines = s.splitlines()

        # Then create a new temporary file to copy the tasks into
        fb, abs_path = tempfile.mkstemp()
        new_file = open(fb, 'w', encoding="utf-8")

        # Copy the old tasks into the new, modifying the updated tasks with the
        # new state
        for line in lines:
            b = line.split(" a:", 2)
            if b[0] == task_txt:
                line = b[0].strip() + " a:1 s:" + self.keywords[index].lower()
                if ( self.keywords[index] == self.end_state )  or ( self.keywords[index] == self.del_state ):
                    line = "x " + time.strftime("%Y-%m-%d") + " " + line
            new_file.write(line + "\n")
        new_file.close()  # mkstemp() path is still available

        # want to bail if we can't make a backup
        try:
            shutil.copy(todo_path, todo_path.replace("txt", "bak"))
        except RuntimeError:
            print("Error creating backup\n")

        # if the backup was successful, remove the old todo file, and move the new
        # one to it
        os.remove(todo_path)
        shutil.move(abs_path, todo_path)

    def run(self, edit):

        settings = sublime.load_settings("Task.sublime-settings")
        self.lead = settings.get('lead')
        self.keywords = settings.get('keywords')
        self.end_state = settings.get('end_state')
        self.del_state = settings.get('del_state')
        self.keywords.extend(['none'])  # Add in option to clear task formatting
        self.formats = settings.get('formats')

        self.view.window().show_quick_panel(self.keywords, self.on_done, 1)


class FormatTask(sublime_plugin.TextCommand):

    def run(self, edit, args):
        self.view.replace(edit, self.view.line(self.view.sel()[0]), args['text'])
