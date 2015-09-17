import sublime_plugin
import sublime
import os


class TraceBackCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        top = sublime.active_window().project_data()['folders'][0]['path']
        a = self.view.file_name()
        a_path = os.path.dirname(a)
        a_file = os.path.basename(a)
        hitMatrix = []
        for root, dirs, files in os.walk(top):
            for fileName in files:
                if fileName.endswith(".md") and os.path.join(root, fileName) != a:  # bypass self
                    relPath = os.path.relpath(a_path, root)
                    relPath = relPath.replace('\\', '/')
                    f = open(os.path.join(root, fileName), encoding='ascii', errors='surrogateescape')
                    fn = int(0)  # Want to reference line number in output
                    for line in f:
                        fn = fn + 1
                        if line.find("--- Traceback Links ---") > (-1):
                            break  # Don't include traceback links as traceback links
                        if line.find(relPath + "/" + a_file) > (-1):
                            relPathBack = os.path.relpath(root, a_path)
                            relPathBack = relPathBack.replace('\\', '/') + "/" + fileName
                            i = "- [" + fileName + "](" + relPathBack + ") - line: " + str(fn) + "\n"
                            hitMatrix.append(i)
        if len(hitMatrix):
            sel_a = self.view.find("\n^--- Traceback Links ---", 0).a
            if sel_a == -1:
                sel_a = self.view.size()
            sel_b = self.view.size()
            self.view.erase(edit, sublime.Region(sel_a, sel_b))
            outStr = "\n--- Traceback Links ---\n\n"
            end = sel_a + self.view.insert(edit, sel_a, outStr)
            outStr = "Found " + str(len(hitMatrix)) + " traceback links:\n\n"
            end = end + self.view.insert(edit, end, outStr)
            for a in hitMatrix:
                end = end + self.view.insert(edit, end, a)
