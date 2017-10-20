import sublime_plugin
import os


class FormIndex(sublime_plugin.TextCommand):

    def run(self, edit):
        # Do path stuff:
        # a is filename without ".md"
        # b is the path
        # bl is list of path components
        # e is project root path
        # el is list of root path components
        b_raw = os.path.dirname(self.view.file_name())
        b = b_raw.replace('\\', '/')
        bl = b.split("/")
        c = self.view.window().project_data()
        d = c['folders'][0]
        e = d['path']
        e = e.replace('\\', '/')
        el = e.split("/")

        ## Put in a header for the index at the current cursor location
        end = self.view.sel()[0].b
        end = end + self.view.insert(edit, end, "## Wiki Index\n")

        # Create path that climbs us the directory structure
        # leading "../" is dropped off in next for loop
        up = ''
        for i in range(1, len(bl)-len(el)+1):
            up = up + '../'

        # Write out the directory links as markdown bullets
        for i in range(len(el)-1, len(bl)-1):
            outStr = '- [' + bl[i] + '](' + up + 'index.md)\n'
            end = end + self.view.insert(edit, end, outStr)
            up = up[3:]

        # If the current directory has an "index.md" (and this isn't
        # it), then put a link to it:
        if (os.path.isfile(os.path.join(b_raw, 'index.md'))
        and os.path.basename(self.view.file_name()) != 'index.md'):
            outStr = '- [' + bl[-1] + '](./index.md)\n'
            end = end + self.view.insert(edit, end, outStr)
