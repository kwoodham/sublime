import sublime_plugin
import sublime
import os
from operator import itemgetter  # 20150729 - support reverse sort (most recent top)

# Looks for occurrences of "stringToFind" in the directory
# of the view or below. Show each in the quick panel - provides
# link to each instance.

# 20171212 - use "lead" as task designation string - load it from the settings file
# change to UTF-8 as funky characters werebombing ascii file read

# 06 Dec 2017 change to use header lead (see note in task toggle)

# 20171106 - change to state in list of states provided from "task_interface"
# https://stackoverflow.com/questions/9542738/python-find-in-list


class ShowInstancesCommand(sublime_plugin.TextCommand):
    newView = int(0)

    def run(self, edit, args):

        settings = sublime.load_settings("Task.sublime-settings")
        lead = settings.get('lead')

        stringToFind = args['text']
        fName = self.view.file_name()
        dName = os.path.dirname(fName)
        self.list = []
        self.matrix = findStr(self, dName, stringToFind, lead)
        if len(self.matrix) != int(0):
            for i in range(0, len(self.matrix)):
                self.list.append(self.matrix[i][2] + ': ' + self.matrix[i][3])
            #  timeout fix at https://github.com/tosher/Mediawiker/blob/master/mediawiker.py
            sublime.set_timeout(lambda: self.view.window().show_quick_panel(self.list, self.on_done), 1)

        else:
            print("None.")

    def on_done(self, index):
        if index == -1:
            return
        self.lineNumb = self.matrix[index][0]
        self.fileName = self.matrix[index][2]  # need to include path
        ShowInstancesCommand.newView = self.view.window().open_file(self.fileName)
        self.center_text(ShowInstancesCommand.newView)

    # See https://www.sublimetext.com/forum/viewtopic.php?f=6&t=14818
    # for use of "is_loading()"
    def center_text(self, view):
        if not ShowInstancesCommand.newView.is_loading():
            view.show_at_center(view.text_point(self.lineNumb, 0))
        else:
            # Half a second should be ample - above ref gives 10 ms
            sublime.set_timeout(lambda: self.center_text(ShowInstancesCommand.newView), 500)


def findStr(self, top, stringToFind, lead):
    p1 = os.path.relpath(os.path.dirname(self.view.file_name()))
    hitMatrix = []
    n = int(0)
    for root, dirs, files in os.walk(top):
        for fileName in files:
            if fileName.endswith(".md"): 
                f = open(os.path.join(root, fileName), encoding='utf-8', errors='surrogateescape')
                fn = 0  # Need to reference line number
                for line in f: 
                    fn = fn + 1                                                                                                                                                
                    if ( line[0:len(lead)] == lead ) and ( line.split(' ')[1] in stringToFind ):
                        # print(line)
                        n = n + int(1)
                        p0 = os.path.relpath(root)
                        relPath = os.path.relpath(p0, p1)
                        relPath = relPath.replace('\\', '/')
                        relFileName = relPath + "/" + fileName
                        line = line.replace(lead,"") # only show keyword and task text - not lead
                        i = [fn, fileName, relFileName, line.rstrip('\n')]
                        hitMatrix.append(i)
    # Return a sorted (most recent first) list
    # see https://wiki.python.org/moin/HowTo/Sorting
    revHitMatrix = sorted(hitMatrix, key=itemgetter(1, 0), reverse=True)
    return(revHitMatrix)
