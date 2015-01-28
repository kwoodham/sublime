import sublime_plugin
import sublime
import os
import glob


class IndexCheckCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = sublime.load_settings("IndexCheck.sublime-settings")
        add_orphan_list = settings.get('add_orphan_list', True)
        ignore_exts = settings.get('ignore_exts', [])

        file_strs = []
        widows = []
        orphans = []
        file_path = os.path.dirname(self.view.file_name())

        if os.path.basename(self.view.file_name()) != 'index.md':
            print('\nThis should be run on an \"index.md\" file. Exiting...')
            return

        # Check [[file]] (file.md in CWD)
        locations = self.view.find_all('\[\[[A-Za-z0-9]')
        loc_lines = [self.view.substr(self.view.line(a)) for a in locations]
        for a in loc_lines:
            l = a.find('[[')
            r = a.find(']]')
            b = "./"+a[(l+2):r]+'.md'
            file_strs.append(b)

        # Check (./file)
        locations = self.view.find_all('\(\.\/[A-Za-z0-9]')
        loc_lines = [self.view.substr(self.view.line(a)) for a in locations]
        for a in loc_lines:
            l = a.find('(')
            r = a.find(')')
            b = a[(l+1):(r+1)]
            if b.find('#'):
                b = b[:b.find('#')]
            file_strs.append(b)

        # Check (../file)
        locations = self.view.find_all('\(\.\.\/[A-Za-z0-9]')
        loc_lines = [self.view.substr(self.view.line(a)) for a in locations]
        for a in loc_lines:
            l = a.find('(')
            r = a.find(')')
            b = a[(l+1):(r+1)]
            if b.find('#'):
                b = b[:b.find('#')]
            file_strs.append(b)

        # Check ([id]: ./file or ../file)
        locations = self.view.find_all('^\[[a-z]+\]\: \.')
        loc_lines = [self.view.substr(self.view.line(a)) for a in locations]
        for a in loc_lines:
            l = a.find('.')
            file_strs.append(a[(l-1):])

        for a in file_strs:
            a_exists = os.path.isfile(os.path.join(file_path, a))
            if not a_exists:
                widows.append(a)

        # Check that all files in directory are referenced

        # Directory file names
        files_abs = glob.glob(file_path+"/*.*")
        files_rel = [os.path.relpath(a, file_path) for a in files_abs]

        # Only want files references in the markdown
        # that are in local directory
        files_loc = []
        for a in file_strs:
            b = a.split('/')
            if (len(b) == 2) and (b[0] == '.'):
                files_loc.append(b[1])

        for a in ignore_exts:
            print(a)

        for a in files_rel:
            print('file is: '+a)
            if not (a in files_loc):
                if (a != 'index.md' and
                    not a.startswith('~') and
                    not (a[a.find("."):] in ignore_exts)):
                    orphans.append(a)

        print('\nYou have '+str(len(widows))+' widows (bad links):\n')
        for a in widows:
            print(a)

        outStr = '\nYou have '+str(len(orphans))
        outStr = outStr+' orphans (unreferenced files)\n'
        print(outStr)
        for a in orphans:
            print(a)

        if (len(orphans) and add_orphan_list):
            sel_a = self.view.find("^--- Orphaned Files ---", 0).a
            if sel_a == -1:
                sel_a = self.view.size()
            sel_b = self.view.size()
            self.view.erase(edit, sublime.Region(sel_a, sel_b))
            outStr = "\n\n--- Orphaned Files ---\n\n"
            end = sel_a + self.view.insert(edit, sel_a, outStr)
            for a in orphans:
                outStr = '- ['+a+'](./'+a+')\n'
                end = end + self.view.insert(edit, end, outStr)
