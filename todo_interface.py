import sublime_plugin
import sublime


class TodoInterfaceCommand(sublime_plugin.TextCommand):

    global l
    global context

    def run(self, edit):

        settings = sublime.load_settings("TodoInterface.sublime-settings")
        todo_path = settings.get('todo_path', True)
        f = open(todo_path, 'r')
        s = f.read()
        f.close()
        TodoInterfaceCommand.l = s.splitlines()

        self.c = []
        for line in TodoInterfaceCommand.l:
            l1 = line.find(' @')  # space before context
            if l1 > 0:
                l1 = l1+1  # move pointer to "@"
                l2 = line.find(' ', l1)
                if l2 < 0:
                    l2 = len(line)
            self.c.append(line[l1:l2])
        self.c = list(set(self.c))
        self.c.sort()
        self.view.window().show_quick_panel(self.c, self.on_done1)

    def on_done1(self, index):

        if index == -1:
            return
        TodoInterfaceCommand.context = self.c[index]

        self.d = []
        for line in TodoInterfaceCommand.l:
            if line.find(self.c[index]) > 0:
                l1 = line.find(' +')  # space eliminates ":+2wk" tag pattern
                if l1 > 0:
                    l1 = l1+1  # move pointer to "+"
                    l2 = line.find(' ', l1)
                    if l2 < 0:
                        l2 = len(line)
                    self.d.append(line[l1:l2])
        if len(self.d) == 0:
            self.d.append('all')
        elif len(self.d) > 1:
            self.d.append('all')
        self.d = list(set(self.d))
        self.d.sort()
        self.view.window().show_quick_panel(self.d, self.on_done2)

    def on_done2(self, index):

        if index == -1:
            return
        project = self.d[index]

        self.e = []

        for line in TodoInterfaceCommand.l:
            if line.find(TodoInterfaceCommand.context) > 0 and (line.find(project) > 0 or project == 'all'):
                self.e.append(line)
        self.view.window().show_quick_panel(self.e, self.on_done3)

    def on_done3(self, index):

        if index == -1:
            return
        self.view.run_command("insert_text", {"args": {'text': self.e[index]}})


class InsertText(sublime_plugin.TextCommand):

    def run(self, edit, args):

        sel = self.view.sel()[0]
        self.view.insert(edit, sel.a, args['text'])
