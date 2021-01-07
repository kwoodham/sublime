import sublime_plugin
import os

# 07 Jan 2021 This version moves to a procedure that can be called. 
# Used in "create_subtopic"

class FormIndex(sublime_plugin.TextCommand):

    def run(self, edit):
        # Do path stuff:
        # a is filename without ".md"
        # b is the path
        # bl is list of path components
        # e is project root path
        # el is list of root path components
        file_arg = self.view.file_name()
        proj_arg = self.view.window().project_data()

        outStr = formIndexProc(file_arg, proj_arg)

        end = self.view.sel()[0].b
        end = end + self.view.insert(edit, end, outStr)


def formIndexProc(file_arg, proj_arg):
    b_raw = os.path.dirname(file_arg)
    b = b_raw.replace('\\', '/')
    bl = b.split("/")
    c = proj_arg
    d = c['folders'][0]
    e = d['path']
    e = e.replace('\\', '/')
    el = e.split("/")


    # Put in a header for the index at the current cursor location
    outStr = "## Wiki Index\n\n"

    # Create path that climbs us the directory structure
    # leading "../" is dropped off in next for loop
    up = ''
    for i in range(1, len(bl) - len(el) + 1):
        up = up + '../'

    # Write out the directory links as markdown bullets
    for i in range(len(el) - 1, len(bl) - 1):
        outStr = outStr + '- [' + bl[i] + '](' + up + 'index.md)\n'
        up = up[3:]

    # If the current directory has an "index.md" (and this isn't
    # it), then put a link to it:
    if (os.path.isfile(os.path.join(b_raw, 'index.md')) and
    os.path.basename(file_arg) != 'index.md'):
        outStr = outStr + '- [' + bl[-1] + '](./index.md)\n'

    return(outStr)
