import sublime_plugin
import sublime
import os


class TraceBackCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        top = top = self.window.project_data()['folders'][0]['path']
        a = self.view.file_name()
        rel_a = os.path.relpath(a,top)
        hitMatrix = []
        n = int(0)
        for root, dirs, files in os.walk(top):
            for fileName in files:
                if fileName.endswith(".md"):
                    f = open(os.path.join(root, fileName), encoding='ascii', errors='surrogateescape')
                    for line in f:
                    if line.find(stringToFind) == (0):  # Only match at start of line
                        n = n + int(1)
                        p0 = os.path.relpath(root)
                        relPath = os.path.relpath(p0, p1)
                        relPath = relPath.replace('\\', '/')
                        relFileName = relPath + "/" + fileName
                        i = [fn, fileName, relFileName, line.rstrip('\n')]
                        hitMatrix.append(i)
    # Return a sorted (most recent first) list
    # see https://wiki.python.org/moin/HowTo/Sorting
    revHitMatrix = sorted(hitMatrix, key=itemgetter(1, 0), reverse=True)
    return(revHitMatrix)

        sRaw = sublime.get_clipboard()
        sParse = sRaw.split('|')
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
