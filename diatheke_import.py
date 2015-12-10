import sublime_plugin
import sublime
import subprocess
import re

# 10 Dec 2015 - if empty selection, then grab the whole line as a reference.  This means that 
# I don't have to select a reference after I just typed it on a new line.  This also means that
# the line should only contain a reference or a chain of references.
# 10 Dec 2015 - add a blank line in between a chain of references

class DiathekeImportCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # Get the reference
        refLoc = self.view.sel()[0]
        if not refLoc.size():  # if selection is not highlighted, assume line is reference(s)
            refLoc = self.view.line(refLoc.a)
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
                end = end + self.view.insert(edit, end, "> " + line + "  \n")
            end = end + self.view.insert(edit, end, "\n") # Add a space between references
        # Place the buffer at the end of the new text, and center the view
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(end))
        self.view.show_at_center(end)


class DiathekeSession:

    def doPassageQuery(self, refTxt):
        P = []
        P.append(['<lb type="x-begin-paragraph"/>', '(br)'])
        P.append(['<lb subType="x-same-paragraph" type="x-begin-paragraph"/>', '(br)'])
        P.append(['<lb type="x-end-paragraph"/>', '(br)'])
        P.append(['<l type="x-indent"/>', ' \t'])
        P.append(['<l type="x-br"/>', '(br)'])
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

        re_str1 = '\s[es]ID\=\"[wx0-9.]+\"'   # Takes care of the eID and sID strings
        re_str2 = '\<[a-zA-Z0-9="/ -]+\>'     # Misc markups that I don't process (just remove)

        argd = "-b ESV -e HTML -k "
        cmds = "diatheke " + argd + refTxt

        text = subprocess.Popen(cmds, shell=True, stdout=subprocess.PIPE).stdout.read()
        text = text.decode("utf-8")
        f = text.split('\n')

        # Do markup replacements and store results in f1
        f1 = []
        for line in f:
            a = re.findall(re_str1, line)
            for instance in a:
                line = line.replace(instance, '')
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
        f3 = []
        new_para = ''
        for line in f2:
            if line.find('\\') > -1:
                line = line.replace('\\', '')
                line = line.strip()
                new_para = new_para + ' ' + line
                new_para = new_para.lstrip()
                new_para = re.sub('[ ]+', ' ', new_para)  # Reduce multiple spaces to one
                f3.append(new_para)
                f3.append('')
                new_para = ''
                last_write = int(1)
            else:
                line = line.strip()
                new_para = new_para + ' ' + line
                last_write = int(0)
        if not last_write:
            new_para = new_para.strip()
            new_para = re.sub('[ ]+', ' ', new_para)  # Reduce multiple spaces to one
            f3.append(new_para)
            f3.append('')

        # Some newlines may have been introduced in markup replacements (e.g x-br) - add
        # these:
        passage = []
        for line in f3:
            line_split = line.split('(br)')
            for new_line in line_split:
                passage.append(new_line.strip(' '))
        return passage

        # passage = []
        # for line in f3:
        #     passage = passage + line.split('(br)')
        # return passage
