# sublime

<!-- MarkdownTOC -->

- [Introduction](#introduction)
- [Wiki Configuration](#wiki-configuration)
- [Set up progression:](#set-up-progression)
- [Adding material](#adding-material)
- [Journal](#journal)
	- [Commands](#commands)
	- [Key bindings](#key-bindings)
- [Other namespaces](#other-namespaces)
	- [Commands](#commands-1)
	- [Key-bindings](#key-bindings-1)
- [Script summary](#script-summary)

<!-- /MarkdownTOC -->


## Introduction

This repository maintains a set of [Sublime Text 3][st3] (hereafter: ST3) scripts that I have developed to manage my personal workflow, using the [ST3 API][api].  The dominant theme here is to set up a "wiki" flavor that allows me to create and capture links between documents and headers (in the same document or other documents).  Additionally, I handle tasks within my pages (outstanding, pending, and done).

All wiki pages are in [Markdown][md]

The "journal" portion of my wiki has one page per week, with day headers pre-populated for each day.  There are a couple scripts for configuring a year's index page, and initializing a week page.

The wiki can be generated and traversed standalone - or it can be rendered into html for local display or pushing to a web server.  I use a `bash` script that wraps a little `sed` around [pandoc][] for rendering.   

## Wiki Configuration

I am in favor of using a file system hierarchy for a wiki rather than a "flat" directory.  This helps me keep the number of files in a directory reasonable, and I don't have to worry about clobbering a file with an identically-named file related to a different topic.  The configuration that has evolved for me is to have an `index.md` file in each directory that provides an anchor for that topic.  I developed a script to populate the index file with links to navigate on up the wiki to the root (see `form_index`), and another script that will check that (a) all the links in the file are valid (i.e. point to a real location) and that all files in the directory are referenced within the index (see `index_check`)

I've also struggled a lot with deciding if I should have a time-oriented wiki (journal) or a project-oriented wiki.  What I've come up with supports both - I have a week-based file that is auto-populated with second-level Markdown headers for days (see `wiki-template`) and can then use a combination of `link-to-heading` and `pase-wiki-link` to generate cross references.  Assigning `open_link_under_cursor` provides a hot-key to jump between tree structures.  So this provides a way to chronicle project activities within the time-based journal, or conversely, reference journal dates/events/conversations within project information.  The root of the system is time-based, and a hot-key assigned to `goto_today` will always take you to the current day's journal heading.

So the directory hierarchy looks something like this:

```
---file system---|
                 |--my wiki--| (sublime project folder)
                 			 | index.md (Top level index page)
                 			 |--201X--| (year journal space)
                 			 		  |--index.md
                 			 		  |--201XMMDD.md (week journals)
                 			 		  |--support folders
                 			 		  |--support files
                 			 |--ProjectA--| (as an example project namespace)
                 			 			  |--index.md
                 			 			  |--support folders
                 			 			  |--support files
                 			 			  |--Namespace folder--|
                 			 			  					   |--index.md
                 			 			   					   |--support folders
                 			 			   					   |--support files
                 			 |--References
                 			 |--Misc
                 			 |--etc...
```
Note that this structure is representative - currently there are only a few "hard-coded" aspects of this structure:

1. The top-level wiki folder is the Sublime Text project folder 
2. There is a "year" folder (e.g. 2015) at the top level of the wiki
3. Each "namespace" folder has an `index.md` in it - this includes the top-level wiki folder, the year folders, and any other top-level folder or lower-level folder with a defined namespace.

Some clarification is necessary on this last point.  In the above hierarchy, I have placeholders for "support folders" and support files.  You can put any folders in the wiki that you want - say for instance you attended a conference and you received all the presentation files: you might have a page that is `conference.md` that captures your notes, and then - just to keep the current directory clean, set up a folder `conference/` and in it place all of the presentation files.  Then in your `conference.md` file you would reference a specific presentation using `[Presentation A](./conference/presentationA-file.ppt)`. Because you are only using `conference/` for local file storage - we're not considering it a namespace, so it's not going to need an `index.md` file in it.

Now, if you set up a project, and know that there will be lots of meetings, files, sub-topics, etc... it's probably wise to consider it as having its own "namespace" and then set up an `index.md` file in it.  This namespace folder can have subfolders (which can in turn be other namespaces), other Markdown files, supporting files, etc...  But the advantage of having an `index.md` file in the directory is that you can use the `index_check` command to make sure that all of the "stuff" in the namespace is referenced.  It's very easy to dump something in a folder, and then not having any wiki content that points to it.

So bottom line - if a directory is just storing a few files (such as the conference presentations referenced above), then just leave it as a simple directory.  But if you intend to use it as the basis for wiki material that will be maintained and added to - treat it as a spacial namespace, and user an `index.md` file to "anchor" the content.

Again, all of this uses the Sublime project folder as the root reference.  This is nice in that if you move the root folder (and with it all of the sub-content), you can relocate the wiki anywhere in your file system: the location of the wiki content is only tied to the root folder of the sublime project.

## Set up progression:

1. Create a folder with your tope level wiki name (suggest not using spaces in folder names, but that's my preference) and put an `index.md` file inside it (file contents not import right now)
2. In ST3, open the folder under `File --> Open Folder...`
3. In ST3, create the project using `Project --> Save Project As`
4. In `index.md` start putting your wiki content in.  That's it

## Adding material

Assuming you are familiar with [Markdown][md], I'll only cover stuff that is unique to this wiki work-flow.

First for internal links, you have a few options:

|                            |                                                                   |
| --                         | --                                                                |
| `[[topic]]`                | This assumes a file named `topic.md` exists in the current folder |
| `[topic](./topic-file.md)` | Same, but option for a different title than the file name         |
| `[topic](./path/index.md)` | Location of anchor file for another namespace                     |

Note that for the last example, The scripts support  only relative paths within the current wiki structure.  So if you put a link in to the file system using absolute paths, or even use relative paths pointing to something outside of the wiki hierarchy, my scripts will likely fail.  Even if they don't you will have a hard time if you move the wiki to another location, or (like me), you keep you wiki synchronize between a few computers using something like SVN or Git.

## Journal

Keeping a time-based system of notes is important to my work-flow.  For me, having a separate page for each day is too much, and I have found that weekly pages is about right. Here are commands and key-bindings that I've developed according to how I like to operate. The commands assume that you are familiar with getting to the command line in ST3 using `(Ctrl-backtick)` 

### Commands

1. Open your `(wiki-root)\201X\index.md` file in a buffer and execute `view.run_command('new_year')`.  This will populate the buffer with a list of week journal file links with the names formed by `YYYYMMDD.md`, grouped by months. Remember to save the buffer when you are all done.

2. Place the cursor on the link for the current week's journal file and execute `view.run_command('open_link_under_cursor')`.  This will open up a blank buffer with the given filename `YYYMMDD.md`

3. Inside the blank `YYYMMDD.md` buffer, execute `view.run_command('wiki_template')` to generate a filled-in heading structure for the week, goals, and daily entries.  Again, remember to save the buffer.

4. You can always get to the current day's entry point using `view.run_command('goto_today')` from anywhere in the wiki.

### Key bindings

A couple of these (`open_link_under_cursor` and `goto_today`) are used a lot, so it's a good idea to bind them to keys.  Set these up any way you want to, but for me, all of my key bindings that are wiki related are prefaced with `ctrl-super-w`.  So these two are:

```
{ "keys": ["ctrl+super+w", "j"], "command": "open_link_under_cursor" },
{ "keys": ["ctrl+super+w", "t"], "command": "goto_today" },
```

Think of the top one as `"[j]ump"` and the bottom as `"[t]oday"`

## Other namespaces

The previous topic addressed time-based journal entries.  Here are some additional commands that can be used in journal entries, or also in other namespaces such as references, projects, subprojects, etc...  Note that we've covered `open_link_under_cursor` and an associated key-binding already - it is an often-used command in any type of namespace with cross-references (not just journals).

### Commands

So you've generated a project or reference file, and you've entered some information that you want to link to another location in your wiki.  Some wiki systems have means to embed a specific "anchor" into a specific location, but I find that it's adequate to use a heading for the reference.  So `link_to_heading` provides a way for me to capture a link to any heading in any page, and then, using `paste_wiki_link` embed that link into any other page.  The reason that there are two commands is that I always want to use a relative path between the links, so I need to (a) capture the link (b) go to the page/location where I want the link to appear, and (c) paste in the link in a way that is aware of the _relative_ proximity between the linked page and the pake in which the link appears.

So execute `link_to_heading` (using `view.run_command()` if you don't set up key bindings), then from the drop down select the heading you want to generate the link for.  Now go over to the page where you want the link to appear and make sure that your cursor is located in the proper location.  Then execute `paste_wiki_link`, the heading text, and a "slugified" version of the heading will be placed in the destination.  _("Slugify" is used to take out Caps, spaces, etc.. to create a contiguous string for the link reference)_

Note that you can alway go to the slugified heading location using your key-bindings to `open_link_under_cursor` - the command understands slugify-ese.  

### Key-bindings

Again, you'll likely create a lot of cross references (why else use a wiki?), so key-bindings come in handy.  Here are my versions, again using my "wiki command" prefix:

```
{ "keys": ["ctrl+super+w", "l"], "command": "link_to_heading" },
{ "keys": ["ctrl+super+w", "p"], "command": "paste_wiki_link" },
```




	{ "keys": ["ctrl+super+w", "o"], "command": "open_in_app" },
	{ "keys": ["ctrl+super+w", "c"], "command": "toc_jump" },
	{ "keys": ["ctrl+super+w", "t"], "command": "goto_today" },
	{ "keys": ["ctrl+super+w", "i"], "command": "form_index" },


## Script summary

| Script                        | Purpose                                                             |
| ----------------------------- | ----------------------------------------------------------          |
| `new_year.py`                 | Generate a year index file with links to each week                  |
| `wiki_template.py`            | Populate a week's page with day headers, etc...                     |
| `form_index.py`               | Paste in a road-map to navigate back up the wiki structure          |
| `index_check.py`              | Check for bad links, widows and orphans                             |
| `IndexCheck.sublime-settings` | Configuration file for index check                                  |
| `OpenInApp.sublime-settings`  | Configuration file for open-in-app                                  |
| `link_to_heading.py`          | Puts a link to the selected heading in the copy/paste buffer        |
| `paste_wiki_link.py`          | Pastes the above link in the selected location as a relative path   |
| `open_in_app.py`              | Opens a particular type of file (ext specific) with defined app     |
| `open_link_under_cursor.py`   | Opens the Markdown file defined under the cursor                    |
| `toc_jump.py`                 | Show list of headings in view - select to center                    |
| `pop_date.py`                 | Give a variety of date and date/time strings to paste into text     |
| `show_instances.py`           | Supports task interface - lists instances of the selected tag       |
| `slugify.py`                  | Supports link development - slugifies the links                     |
| `task_interface.py`           | Select @task, @done, or @pending task list in the current namespace |
| `goto_today.py`               | Pop to current week journal page and advance to correct day heading |




[st3]: http://www.sublimetext.com/3
[api]: http://www.sublimetext.com/docs/3/api_reference.html
[md]: http://daringfireball.net/projects/markdown/syntax
[pandoc]: http://johnmacfarlane.net/pandoc/
