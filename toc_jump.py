import sublime_plugin
import sublime
import re
from User.slugify import slugify


class TocJumpCommand(sublime_plugin.TextCommand):

    def on_done(self, index):
        if index == -1:
            return
        self.view.run_command("goto_toc_link",
            {"args": {'text': self.list[index]}})

    def run(self, edit):
        locations = self.view.find_all('^[\#]+')
        self.list = [self.view.substr(self.view.line(a)) for a in locations]
        self.view.window().show_quick_panel(self.list, self.on_done)


class GotoTocLink(sublime_plugin.TextCommand):

    def run(self, edit, args):
        locations = self.view.find_all('^[\#]+')
        while len(locations):
            location = locations.pop(0)
            loc_text = self.view.substr(self.view.line(location))
            if loc_text == args['text']:
                self.view.show_at_center(location)
                return
