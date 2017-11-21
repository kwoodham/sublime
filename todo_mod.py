import sublime_plugin
import sublime
import shutil
import tempfile
import os
import re

def todo_mod(task, target, change):

	    settings = sublime.load_settings("TodoInterface.sublime-settings")
        todo_path = settings.get('todo_path', True)
        f = open(todo_path, 'r')
        s = f.read()
        f.close()

        fb, abs_path = tempfile.mkstemp()
        new_file = open(fb, 'w', encoding="utf-8")

        l = s.splitlines()

        for line in l:
        	if line == l:
				l.replace(target,change)
			new_file.write(l+"\n")

        try:
            shutil.copy(todo_path, todo_path.replace("txt","bak"))
        except:
            print("Error creating backup\n")

        # if the backup was successful, remove the old todo file, and move the new one to it
        os.remove(todo_path)
        shutil.move(abs_path,todo_path)
