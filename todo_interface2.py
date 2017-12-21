import sublime_plugin
import sublime
import shutil
import tempfile
import os


# 15 Nov 2017
# This version looks only for lines that do not contain assigned:1 tags in the todo file
# and displays them for selection.  It then writes the tag onto the task if the task is
# copied into the wiki
# Ref: https://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python

class TodoInterface2Command(sublime_plugin.TextCommand):

    global l
    global todo_path

    def run(self, edit):

        settings = sublime.load_settings("TodoInterface.sublime-settings")
        TodoInterface2Command.todo_path = settings.get('todo_path', True)
        f = open(TodoInterface2Command.todo_path, 'r')
        s = f.read()
        f.close()
        
        TodoInterface2Command.l = s.splitlines()

        # Find all unassigned tasks
        self.c = []
        for line in TodoInterface2Command.l:
            l1 = line.find(' a:1')
            if l1 == -1:
                self.c.append(line)
        self.c.sort()
        TodoInterface2Command.l = self.c

        # Find the list of projects for for the list of unassigned tasks
        self.d = []
        for line in self.c:
            l1 = line.find(' +')  # space eliminates ":+2wk" tag pattern
            if l1 > 0:
                l1 = l1+1  # move pointer to "+"
                l2 = line.find(' ', l1)
                if l2 < 0:
                    l2 = len(line)
                self.d.append(line[l1:l2])
        self.d.append('all')
        self.d = list(set(self.d))
        self.d.sort()
        self.view.window().show_quick_panel(self.d, self.on_done2)

    def on_done2(self, index):

        if index == -1:
            return
        project = self.d[index]

        self.e = []

        for line in TodoInterface2Command.l:
            if  (line.find(project) > 0 or project == 'all'): # Don't need context anymore
                self.e.append(line)
        self.view.window().show_quick_panel(self.e, self.on_done3)

    def on_done3(self, index):

        if index == -1:
            return
        self.view.run_command("insert_text", {"args": {'text': self.e[index]}})


        # Need to recreate the full list of tasks 
        fo = open(TodoInterface2Command.todo_path, 'r', encoding="utf-8")
        s = fo.read()
        fo.close()
        l = s.splitlines()

        # Create a new temporary file
        fb, abs_path = tempfile.mkstemp()
        new_file = open(fb, 'w', encoding="utf-8")

        # Copy the old file into the new, tagging the select task
        for line in l:
            if line == self.e[index]:
                new_file.write(line + " a:1 s:none\n")
            else:
                new_file.write(line + "\n")
        new_file.close() # mkstemp() path is still available

        # want to bail if we can't make a backup
        try:
            shutil.copy(TodoInterface2Command.todo_path, TodoInterface2Command.todo_path.replace("txt","bak"))
        except:
            print("Error creating backup\n")

        # if the backup was successful, remove the old todo file, and move the new one to it
        os.remove(TodoInterface2Command.todo_path)
        shutil.move(abs_path,TodoInterface2Command.todo_path)
       

class InsertText(sublime_plugin.TextCommand):

    def run(self, edit, args):

        sel = self.view.sel()[0]
        self.view.insert(edit, sel.a, args['text'])
