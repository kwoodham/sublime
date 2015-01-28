import sublime_plugin
import sublime
import os

# Looks for occurances of "stringToFind" in the directory
# of the view or below. Show each in the quick panel - provides
# link to each instance.


class ShowInstancesCommand(sublime_plugin.TextCommand):
    newView = int(0)

    def run(self, edit, args):

        stringToFind = args['text']
        fName = self.view.file_name()
        dName = os.path.dirname(fName)
        self.list = []
        self.matrix = findStr(self, dName, stringToFind)
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
        self.fileName = self.matrix[index][1]
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

def findStr(self, top, stringToFind):
    p1 = os.path.relpath(os.path.dirname(self.view.file_name()))
    hitMatrix = []
    n = int(0)
    for root, dirs, files in os.walk(top):
        for fileName in files:
            if fileName.endswith(".md"):
                f = open(os.path.join(root, fileName), encoding='ascii', errors='surrogateescape')
                fn = 0  # Need to reference line number
                for line in f:
                    fn = fn + 1
                    if line.find(stringToFind) != (-1):
                        n = n + int(1)
                        p0 = os.path.relpath(root)
                        relPath = os.path.relpath(p0, p1)
                        relPath = relPath.replace('\\', '/')
                        relFileName = relPath + "/" + fileName
                        i = [fn, fileName, relFileName, line.rstrip('\n')]
                        hitMatrix.append(i)
    return(hitMatrix)
