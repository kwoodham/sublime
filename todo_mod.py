import sublime
import shutil
import tempfile
import os
import datetime

def todo_mod(task, target, change):

    todo_path = sublime.load_settings("TodoInterface.sublime-settings").get("todo_path")
    todo_bak_path = sublime.load_settings("TodoInterface.sublime-settings").get("todo_bak_path")


    f = open(todo_path, 'r')
    s = f.read()
    l = s.splitlines()
    f.close()

    fb, abs_path = tempfile.mkstemp()
    new_file = open(fb, 'w', encoding="utf-8")

    for line in l:
        if line == task:
            line.replace(target,change)
        new_file.write(line+"\n")
    new_file.close()

    t = datetime.datetime.utcnow()
    t_str = str(t.year)+str(t.month)+str(t.day)+str(t.hour)+str(t.minute)+str(t.second)

    try:
        shutil.copy(todo_path, todo_bak_path + t_str + "_todo.bak")
    except:
        print("Error creating backup\n")

    # if the backup was successful, remove the old todo file, and move the new one to it
    os.remove(todo_path)
    shutil.move(abs_path,todo_path)
    return 