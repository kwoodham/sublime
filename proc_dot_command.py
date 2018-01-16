import sublime_plugin
import subprocess
import os
import tempfile
from User.slugify import slugify

# https://www.programcreek.com/python/example/84621/pydot.graph_from_dot_data
# https://stackoverflow.com/questions/5316206/converting-dot-to-png-in-python
# https://github.com/erocarrera/pydot

# Processes text of form: (output is slugified graph name)
# digraph G {
# 	foo -> bar;
# 	bar -> foo;
#    foo -> bas;
#    bar -> bas;
# }


# requires paths to python exec and proc_dot.py

# 12 Jan 2018  - first revision


class ProcDotCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        sel = self.view.sel()[0]
        if len(self.view.substr(sel)) == 0:
            print("Nothing highlighted!")
            return

        sRaw = self.view.substr(sel)
        sRaw = sRaw.splitlines()

        # Check that the right things are in the header line
        if sRaw[0].split(' ')[1] == "{":
            print("Need to name the graph")
            return

        # Then create a new temporary file to copy the tasks into
        # Note mkstemp does not delete the file when it is closed
        fb, abs_path = tempfile.mkstemp()
        new_file = open(fb, 'w', encoding="utf-8")

        # Write dot out to the temp file so the path cam be passed to the script
        for line in sRaw:
            new_file.write(line + "\n")
        new_file.close()  # mkstemp() path is still available

        # Set up the absolute paths for python, the script, and the filename
        python = "C:\\anaconda3\\python.exe"
        script = "C:\\msys64\\home\\kpwoodha\\.local\\bin\\proc_dot.py"
        filename = slugify(sRaw[0].split(' ')[1], "-") + ".png"
        filename = os.path.dirname(self.view.file_name()) + "\\" + filename
        print("Dot output in:\n" + filename)

        # execute the command - script takes dot string and file name as arguments
        command = ["cmd.exe", "/c", python, script, abs_path, filename]
        x = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Extract the standard output or error and print it to console
        stddata = x.communicate()
        output = stddata[0].decode('ascii')
        output = output.splitlines()
        for line in output:
            print(line)

        # delete the temp file
        os.remove(abs_path)
