import sublime_plugin
import sublime
import subprocess
import re

# 27 Apr 2019 - split multiple references by comma or semicolon
# 27 Apr 2019 - Reserve last book name to use if next ref is just chapter and verse
# 27 Apr 2019 - Found the "-f plain" switch - which eliminates all the markup

# 13 Apr 2019 - got going on my Windows laptop had to change bible to ESV2011

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

        refTxt = re.split("[,;] ", self.view.substr(refLoc)) # space is important
        for ref in refTxt:
 
            # 27 Apr 2019 - handle repeat references from the same book: Gen 1:15, 3:14  
            if re.match("[0-9-]+\:[0-9-]+", ref) == None: # Pass is "Gen 1:15"
                [oldBook, NULL] = ref.rsplit(' ', 1)
            else:
                ref = oldBook + ' ' + ref
            # Get the text for the reference (remove the last blank line)
            bible = DiathekeSession()
            passage = bible.doPassageQuery(ref)
            while passage[-1] == '':  # pythony way to reference last element of the list
                passage = passage[:len(passage)-1]

            # Reference may have been highlighted using right-to-left mouse motion
            # and we want to use the right-most point of the region to start adding text
            for line in passage:
                end = end + self.view.insert(edit, end, "> " + line + "  \n")
            end = end + self.view.insert(edit, end, "\n") # Add a space between references
        # Place the buffer at the end of the new text, and center the view
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(end))
        self.view.show_at_center(end)


class DiathekeSession:

    def doPassageQuery(self, refTxt):
        argd = "-b ESV2011 -f plain -k "
        cmds = "diatheke " + argd + refTxt

        text = subprocess.Popen(cmds, shell=True, stdout=subprocess.PIPE).stdout.read()
        text = text.decode("utf-8")
        f = text.split('\n')

        # This used to be a bunch of markup replacements - but I found the "-f plain"
        # switch - so all I do is pull out the translation designation
        f1 = []
        for line in f:
            line = line.replace('(ESV2011)', '')
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
                line = line.strip()
                new_para = new_para + ' ' + line
                last_write = int(0)
        if not last_write:
            new_para = new_para.strip()
            new_para = re.sub('[ ]+', ' ', new_para)  # Reduce multiple spaces to one
            passage.append(new_para)
            passage.append('')

        return passage
