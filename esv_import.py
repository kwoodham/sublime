import sublime_plugin
import sublime
import urllib

# Using Python example from http://www.esvapi.org/api/#sample
# Kurt Woodham
# 17 Sep 2015


class EsvImportCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # Get the reference
        refLoc = self.view.sel()[0]
        refTxt = self.view.substr(refLoc)

        # Get the text for the reference (remove the last blank line)
        bible = ESVSession('IP')
        pssge = bible.doPassageQuery(refTxt)
        pssge = pssge.decode("utf-8")
        pssge = pssge.split("\n")
        if pssge[-1] == '':  # pythony way to reference last element of the list
            pssge = pssge[:len(pssge)-1]

        # Reference may have been hilighted using right-to-left mouse motion
        # and we want to use the right-most point of the region to start
        # adding text
        end = max(refLoc.a, refLoc.b)

        # My preference is to use literal (code) block hilighting
        # particularly because the ESV text comes back with hard-coded returns
        # and I don't want the markdown renderer to join them together
        end = end + self.view.insert(edit, end, "\n\n~~~\n")
        for line in pssge:
            end = end + self.view.insert(edit, end, line + "\n")
        end = end + self.view.insert(edit, end, "~~~\n\n")

        # Place the buffer at the end of the new text, and center the view
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(end))
        self.view.show_at_center(end)


class ESVSession:

    def __init__(self, key):
        options = ['include-short-copyright=0',
                   'output-format=plain-text',
                   'include-passage-horizontal-lines=0',
                   'include-heading-horizontal-lines=0']
        self.options = '&'.join(options)
        self.baseUrl = 'http://www.esvapi.org/v2/rest/passageQuery?key=%s' % (key)

    def doPassageQuery(self, passage):
        passage = passage.split()
        passage = '+'.join(passage)
        url = self.baseUrl + '&passage=%s&%s' % (passage, self.options)
        page = urllib.request.urlopen(url)
        return page.read()
