import sublime_plugin
from User.slugify import slugify

# Assume link is of form:
# 	type 1: [[file without .md in cwd]]
# 	type 2: [text](./relative/path/to/file.md)
# 	type 3: [#link internal to current file]
# 	type 4: [text describing internal link](#slug)
#   type 5: [text describing external link](./path.md#slug)

# Assume that cursor is in the path or slug if last two forms
# Assume that link is correctly formed
# Assume that the path start with "." (always relative) and ends in ".md"
# assume that links of type "[ref]:" are enclosed with "( )"

# MOD1
# Monday, August 03, 2015 - added in logic to link to heading of form:
# ## This is a heading {#anchor}

# MOD2
# Thursday, February 02, 2017 - add in links of type:
# [ref]: (link is here) which are variants of type 2 and 5


class OpenLinkUnderCursorCommand(sublime_plugin.TextCommand):
    link = str('')

    def run(self, edit):

        sel = self.view.sel()[0]
        text = self.view.substr(self.view.line(sel))
        position = self.view.rowcol(sel.begin())[1]

        # Determine the type
        lType = link_type(text, position)

        # Determine the path ends and link ends
        index = set_point(lType, text, position)

        if lType == 1:
            pathName = text[(index[0]+1):index[1]]+'.md'
            OpenLinkUnderCursorCommand.link = None
            self.view.window().open_file(pathName)
        elif lType == 2:
            pathName = text[(index[0]+1):index[1]]
            OpenLinkUnderCursorCommand.link = None
            self.view.window().open_file(pathName)
        elif lType == 3:
            self.link = slugify(text[(index[2]+1):index[3]], '-')
            set_location(self.view, self.link)
        elif lType == 4:
            self.link = slugify(text[(index[2]+1):index[3]], '-')
            set_location(self.view, self.link)
        else:
            pathName = text[(index[0]+1):index[1]]
            self.link = slugify(text[(index[2]+1):index[3]], '-')
            isView = self.view.window().find_open_file(pathName)
            if isView:
                self.view.window().focus_view(isView)
                activeView = self.view.window().active_view()
                set_location(activeView, self.link)
            else:
                OpenLinkUnderCursorCommand.link = self.link
                self.view.window().open_file(pathName)


class EventListener(sublime_plugin.EventListener):

    def on_load_async(self, view):
        set_location(view, OpenLinkUnderCursorCommand.link)
        OpenLinkUnderCursorCommand.link = None


def set_point(lType, text, position):
    lPath = int(0)
    rPath = int(0)
    lLink = int(0)
    rLink = int(0)
    if lType == 1:
        lPath = text.rfind("[[", 0, position)+int(1)
        rPath = text.find("]]", position)
    elif lType == 2:
        lPath = text.rfind("(", 0, position)
        rPath = text.find(")", position)
    elif lType == 3:
        lLink = text.rfind("[", 0, position)
        rLink = text. find("]", position)
    elif lType == 4:
        lLink = text.rfind("#", 0, position)
        rLink = text. find(")", position)
    else:  # type 5
        lLink = text.rfind("#", 0, position)  # Try cursor in slug
        if lLink == -1:
            lLink = text.find("#", position)  # cursor is in path
        rLink = text.find(")", position)
        lPath = text.rfind("(", 0, position)
        rPath = text.rfind("#", 0, position)  # Try cursor in slug
        if rPath == -1:
            rPath = text.find("#", position)  # Cursor is in path
    return [lPath, rPath, lLink, rLink]


def set_location(view, link):
    locations = view.find_all('^[\#]+')
    while len(locations):
        location = locations.pop(0)
        str_line = view.substr(view.line(location.end()))
        a = str_line.rfind('{#')  # Check first for a hard-coded anchor
        if a == -1:
            slug = slugify(str_line, '-')
        else:
            b = str_line.rfind('}')
            slug = str_line[(a+2):b]
        if slug == link:
            view.show_at_center(location)
            return


def link_type(text, position):
    b1 = text.rfind("[", 0, position)       # every type starts with "["
    if text.rfind("[[", b1-1, b1+1) != -1:  # type 1 has "[[" at start
        lType = int(1)
    elif text.rfind("](#", b1, position) != -1:
        lType = int(4)                      # type 4 has "](#" in middle
        # MOD2 - add in allowance for type "]: ("
    elif ( text.rfind("](.", b1, position) ) or ( text.rfind("]: (.", b1, position) ) != -1:
        # have type 2 or 5 depending on "#" before closing ")"
        b2 = text.find(")", position)
        if text.find("#", b1, b2) != -1:
            lType = int(5)                  # type 5 has slug
        else:
            lType = int(2)                  # type 2 doesn't
    else:
        lType = int(3)                      # only thing left
    return lType
