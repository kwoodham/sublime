import sublime_plugin
import sublime
import os


# 2017-12-06 - Change processing of link names to escape the initial "@"
# for tasks - links won't render properly otherwise


class PasteWikiLinkCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sRaw = sublime.get_clipboard()
        sParse = sRaw.split('|')
        if sParse[0][0] == "@": # Handle task links
            sParse[0] = "\\{}".format(sParse[0]) 
        anchorFile = self.view.file_name()
        targetFile = sParse[1]
        if anchorFile == targetFile:
            outStr = '[' + sParse[0] + '](#' + sParse[2] + ')'
        else:
            p1 = os.path.relpath(os.path.dirname(targetFile))
            p2 = os.path.relpath(os.path.dirname(anchorFile))
            f2 = os.path.basename(targetFile)
            relPath = os.path.relpath(p1, p2)
            relPath = relPath.replace('\\', '/')
            outStr = '[' + sParse[0] + ']'
            outStr = outStr + '(' + relPath + '/' + f2
            outStr = outStr + '#' + sParse[2] + ')'
        sel = self.view.sel()
        self.view.insert(edit, sel[0].b, outStr)
