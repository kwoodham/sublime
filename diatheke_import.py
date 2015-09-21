import sublime_plugin
import sublime
import subprocess
import re


class DiathekeImportCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # Get the reference
        refLoc = self.view.sel()[0]
        end = max(refLoc.a, refLoc.b)
        end = end + self.view.insert(edit, end, "\n\n")

        refTxt = self.view.substr(refLoc)
        refTxt = refTxt.split(", ")
        for ref in refTxt:

            # Get the text for the reference (remove the last blank line)
            bible = DiathekeSession()
            pssge = bible.doPassageQuery(ref)
            while pssge[-1] == '':  # pythony way to reference last element of the list
                pssge = pssge[:len(pssge)-1]

            # Reference may have been hilighted using right-to-left mouse motion
            # and we want to use the right-most point of the region to start
            # adding text

            for line in pssge:
                end = end + self.view.insert(edit, end, "> " + line + "\n")

        # Place the buffer at the end of the new text, and center the view
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(end))
        self.view.show_at_center(end)


class DiathekeSession:

    def doPassageQuery(self, refTxt):
        P = []
        P.append(['<lb type="x-begin-paragraph"/>', ''])
        P.append(['<lb type="x-end-paragraph"/>', '\\'])
        P.append(['<q marker="">', ''])
        P.append(['</q>', ''])
        P.append(['<milestone marker="&#8220;" type="cQuote"/>', '"'])
        P.append(['<milestone marker="&#8221;" type="cQuote"/>', '"\\'])
        P.append(['<q level="1" marker="&#8220;"/>', '"'])
        P.append(['<q level="1" marker="&#8221;"/>', '"\\'])
        P.append(['<q level="2" marker="&#8216;"/>', "'"])
        P.append(['<q level="2" marker="&#8217;"/>', "'"])
        P.append(['&#8212;', '--'])
        P.append(['(ESV)', ''])

        re_str1 = '\s[es]ID\=\"[0-9.]+\"'   # Takes care of the eID and sID strings
        re_str2 = '\<[a-zA-Z0-9="/ -]+\>'   # Misc markups

        argd = "-b ESV -e HTML -k "
        cmds = "diatheke " + argd + refTxt

        text = subprocess.Popen(cmds, shell=True, stdout=subprocess.PIPE).stdout.read()
        text = text.decode("utf-8")
        f = text.split('\n')

        # Do markup replacements and store results in f1
        f1 = []
        for line in f:
            line = re.sub(re_str1, '', line)
            for i in range(0, len(P)):
                line = line.replace(P[i][0], P[i][1])
            line = re.sub(re_str2, ' ', line)
            f1.append(line)

        # Only want verse numbers if book and chapter haven't change
        # from the previous line
        f2 = []
        book_chap = ''
        for line in f1:
            if line[0:line.find(':')] == book_chap:
                line = line.replace(line[0:(line.find(':')+1)], '')
            else:
                book_chap = line[0:line.find(':')]
            f2.append(line)

        # Want consecutive verses in paragraphs if no hard-coded
        # breaks are at the end of the verse
        passage = []
        new_para = ''
        for line in f2:
            if line.find('\\') > -1:
                line = line.replace('\\', '')
                line = line.strip()
                new_para = new_para + ' ' + line
                new_para = new_para.lstrip()
                new_para = re.sub('[ ]+', ' ', new_para)  # Reduce multiple spaces to one
                passage.append(new_para)
                passage.append('')
                new_para = ''
                last_write = int(1)
            else:
                line = line.lstrip()
                new_para = new_para + ' ' + line
                last_write = int(0)
        if not last_write:
            new_para = new_para.lstrip()
            new_para = re.sub('[ ]+', ' ', new_para)  # Reduce multiple spaces to one
            passage.append(new_para)
            passage.append('')
        return passage
