import sublime
import sublime_plugin
import random
import datetime

# generate a unique anchor from a date string and the
# decimal portion of a random. Use this for linking
# to headers that seek to give slugify a hard time

class UniqueAnchorCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		random.seed() # uses current time
		a = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
		b = str(random.random()).split(".")[1]
		sel = self.view.sel()[0]
		self.view.insert(edit, sel.a, " {#a" + a + b + "}")
