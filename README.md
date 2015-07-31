# sublime

<!-- MarkdownTOC -->

- [Introduction](#introduction)
- [Wiki Configuration](#wiki-configuration)
- [Setting up the wiki](#setting-up-the-wiki)
- [Adding material](#adding-material)
- [Journaling](#journaling)
        - [Commands](#commands)
        - [Key bindings](#key-bindings)
- [Referencing other namespaces](#referencing-other-namespaces)
        - [Commands](#commands-1)
        - [Key-bindings](#key-bindings-1)
- [Other commands](#other-commands)
        - [Key bindings](#key-bindings-2)
- [Checking the index.md file](#checking-the-indexmd-file)
- [Tasks](#tasks)
- [Post-processing](#post-processing)
- [Summary](#summary)
- [Release](#release)
- [Script summary](#script-summary)

<!-- /MarkdownTOC -->


<a name="introduction"></a>
## Introduction

This repository maintains a set of [Sublime Text 3][st3] (hereafter: ST3) Python scripts that I  developed to manage my personal workflow using the [ST3 API][api].  My intent was to set up a "wiki" capability that allows me to create and capture links between documents and headers (in the same document or other documents) and handle tasks within my pages (outstanding, pending, and done).

All wiki pages are in [Markdown][md].

The "journal" portion of my wiki has one page per week, with day headers pre-populated for each day.  There are a couple scripts for configuring a year's index page, initializing a week page, and to quickly return to the current day's entry from anywhere in the wiki structure.

The wiki can be generated and traversed standalone - or it can be rendered into HTML for local display or pushing to a web server.  I use a `bash` script that wraps a little [sed][] around [pandoc][] for rendering.   

<a name="wiki-configuration"></a>
## Wiki Configuration

I am in favor of using a file system hierarchy for a wiki rather than a "flat" directory.  This helps me keep the number of files in a directory reasonable, and I don't have to worry about clobbering a file with an identically-named file related to a different topic.  The configuration that has evolved for me is to have an `index.md` file in each directory that provides an anchor for that topic.  I developed a script to populate the index file with links to navigate on up the wiki to the root (see `form_index`), and another script that will check that (a) all the links in the file are valid (i.e. point to a real location) and that all files in the directory are referenced within the index (see `index_check`)

I've also struggled a lot with deciding if I should have a time-oriented wiki (journal) or a project-oriented wiki.  What I've come up with supports both - I have a week-based file that is auto-populated with second-level Markdown headers for days (see `wiki-template`) and can then use a combination of `link-to-heading` and `pase-wiki-link` to generate cross references.  Assigning `open_link_under_cursor` provides a hot-key to jump between tree structures.  So this provides a way to chronicle project activities within the time-based journal, or conversely, reference journal dates/events/conversations within project information.  The root of the system is time-based, and a hot-key assigned to `goto_today` will always take you to the current day's journal heading.

So the directory hierarchy looks something like this:

```
---file system---|
                 |--my wiki--|
                             |--index.md 
                             |--201X--| 
                                      |--index.md
                                      |--201XMMDD.md 
                                      |--support folders
                                      |--support files
                             |--ProjectA--| 
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

Note that this structure is representative - currently there are only a handful of "hard-coded" aspects of this structure that you should constrain yourself to if you want all of the wiki commands to work:

1. The top-level wiki folder is the Sublime Text project folder 
2. There is a "year" folder (e.g. 2015) at the top level of the wiki
3. Each "namespace" folder has an `index.md` in it - this includes the top-level wiki folder, the year folders, and any other top-level folder or lower-level folder with a defined namespace.

Some clarification is necessary on this last point.  In the above hierarchy, I have show support folders and support files in each of the namespace folders.  You can drop any type of file in any of the folders and then link to it from within the `index.md` file or any other markdown file in the directory.  Say for instance you attended a conference and you received all the presentation files: you might have a page that is `conference.md` that captures your notes, and then - just to keep the current directory clean, set up a folder `conference/` and in it place all of the presentation files.  Then in your `conference.md` file you would reference a specific presentation using `[Presentation A](./conference/presentationA-file.ppt)`, and then in your `index.md` file  that might relate to a specific project, you put in a link to `conference.md` as an important conference that pertains to the project. Because you are only using `conference/` for local file storage, we're not considering it a namespace, so it probably doesn't make sense to put an `index.md` file in it.

__"So why `index.md` and not some other name?__  In my system I give the the namespace folder a descriptive name already, so I don't need to also give the anchor file a descriptive name as well.  So to me a `[Systems Engineering Reference](./references/systems-engineering/index.md)` link makes more sense than a `[Systems Engineering Reference](./references/directory2/systems-engineering.md)` link, where I don't have any idea about the purpose of `directory2` unless I look inside.  When I'm using my file explorer to find the right folder to drop something into, it helps to have descriptive folder names; and if I have descriptive folder names, I don't have to double-up by having a descriptive anchor file name.  So I chose `index.md`.  You can use whatever you want, but the advantage of using `index.md` is that you can use the `index_check` command (which assumes the existence of an `index.md` file) to make sure that all of the "stuff" in the namespace is referenced.  It's very easy to dump something in a folder, and then not having any wiki content that points to it.  

So if you set up a project and know that there will be lots of associated meetings, files, sub-topics, etc... it's probably wise to consider it as having its own "namespace" (project folder) and then have an `index.md` file in it.  This namespace folder can have subfolders (which can be other namespaces), other Markdown files, supporting files, etc...  

Again, all of this uses the Sublime project folder as the root reference.  This is nice in that if you move the root folder (and with it all of the sub-content), you can relocate the wiki anywhere in your file system: the location of the wiki content is only tied to the root folder of the sublime project.

<a name="setting-up-the-wiki"></a>
## Setting up the wiki

1. Create a folder with your top level wiki name (suggest not using spaces in folder names, but that's my preference) and put an `index.md` file inside it (file contents not import right now)
2. In ST3, open the folder under `File --> Open Folder...`
3. In ST3, create the project using `Project --> Save Project As`
4. In `index.md` start putting your wiki content in.  Maybe the first line is the Wiki Header using a level 1 header `"#"`, then some descriptions, then links to other Markdown files and namespaces below this top level.  That's it!

<a name="adding-material"></a>
## Adding material

Assuming you are familiar with [Markdown][md], I'll only cover stuff that is unique to this wiki work-flow.

First for internal links, you have a few options:

| Form                       | Description                                                       |
| -----                      | -----                                                             |
| `[[topic]]`                | This assumes a file named `topic.md` exists in the current folder |
| `[topic](./topic-file.md)` | Same, but option for a different title than the file name         |
| `[topic](./path/index.md)` | Location of anchor file for another namespace                     |

Note that for the last example, The scripts support  only relative paths within the current wiki structure.  So if you put a link in to the file system using absolute paths, or even use relative paths pointing to something outside of the wiki hierarchy, my scripts will likely fail.  Even if they don't you will have a hard time if you move the wiki to another location, or (like me), you keep you wiki synchronize between a few computers using something like SVN or Git.

_(You can also link to other headings in the same file or in a different file. This is covered below under [Referencing other namespaces](#referencing-other-namespaces). In other words, you don't have to restrict links to the file level, but can link to specific locations within other Markdown files.)_

<a name="journaling"></a>
## Journaling

Keeping a time-based system of notes is important to my work-flow.  For me, having a separate page for each day is too much, and I have found that weekly pages is about right. Here are commands and key-bindings that I've developed according to how I like to operate. The commands assume that you are familiar with getting to the command line in ST3 using `(Ctrl-backtick)` 

<a name="commands"></a>
### Commands

1. Open your `(wiki-root)\201X\index.md` file in a buffer and execute `view.run_command('new_year')`.  This will populate the buffer with a list of week journal file links with the names formed by `YYYYMMDD.md`, grouped by months. Remember to save the buffer when you are all done.

2. Place the cursor on the link for the current week's journal file and execute `view.run_command('open_link_under_cursor')`.  This will open up a blank buffer with the given filename `YYYMMDD.md`

3. Inside the blank `YYYMMDD.md` buffer, execute `view.run_command('wiki_template')` to generate a filled-in heading structure for the week, goals, and daily entries.  Again, remember to save the buffer.

4. You can always get to the current day's entry point using `view.run_command('goto_today')` from anywhere in the wiki.

<a name="key-bindings"></a>
### Key bindings

A couple of these (`open_link_under_cursor` and `goto_today`) are used a lot, so it's a good idea to bind them to keys.  Set these up any way you want to, but for me, all of my key bindings that are wiki related are prefaced with `ctrl-super-w`.  So these two are:

```
{ "keys": ["ctrl+super+w", "j"], "command": "open_link_under_cursor" },
{ "keys": ["ctrl+super+w", "t"], "command": "goto_today" },
```

Think of the top one as `"[j]ump"` and the bottom as `"[t]oday"`

<a name="referencing-other-namespaces"></a>
## Referencing other namespaces

The previous topic addressed time-based journal entries.  Here are some additional commands that can be used in journal entries, or also in other namespaces such as references, projects, subprojects, etc...  Note that we've covered `open_link_under_cursor` and an associated key-binding already - it is an often-used command in any type of namespace with cross-references (not just journals).

<a name="commands-1"></a>
### Commands

So you've generated a project or reference file, and you've entered some information that you want to link to another location in your wiki.  Some wiki systems have means to embed a specific "anchor" into a specific location, but I find that it's adequate to use a heading for the reference.  So `link_to_heading` provides a way for me to capture a link to any heading in any page, and then, using `paste_wiki_link` embed that link into any other page.  The reason that there are two commands is that I always want to use a relative path between the links, so I need to (a) capture the link (b) go to the page/location where I want the link to appear, and (c) paste in the link in a way that is aware of the _relative_ proximity between the linked page and the pake in which the link appears.

So execute `link_to_heading` (using `view.run_command()` if you don't set up key bindings), then from the drop down select the heading you want to generate the link for.  Now go over to the page where you want the link to appear and make sure that your cursor is located in the proper location.  Then execute `paste_wiki_link`, the heading text, and a "slugified" version of the heading will be placed in the destination.  _("Slugify" is used to take out Caps, spaces, etc.. to create a contiguous string for the link reference)_

Note that you can alway go to the slugified heading location using your key-bindings to `open_link_under_cursor` - the command understands slugify-ese.  

<a name="key-bindings-1"></a>
### Key-bindings

Again, you'll likely create a lot of cross references (why else use a wiki?), so key-bindings come in handy.  Here are my versions, again using my "wiki command" prefix:

```
{ "keys": ["ctrl+super+w", "l"], "command": "link_to_heading" },
{ "keys": ["ctrl+super+w", "p"], "command": "paste_wiki_link" },
```

<a name="other-commands"></a>
## Other commands

Here are a few additional commands that I've conjured up to support other things that I do a lot.

If you are in a large file, and need to go to some other location in the file, use `toc_jump` to select another heading in the file and jump to it.  Pretty useful if you have a big file and want to more around in it.  

_(Note: the ST3 package `MarkdownTOC` maintains an on-the-fly table of contents at the selected location in the file--like the one at the top of this readme.  This can be configured to provide "slugified" links to the headers, and so - using my `open_link_under_cursor` command, you can replicate much of what is done in `toc_jump`. You can use either approach - or both)_

When your directory structure gets to be farily complex, you need to have some means for navigating back up the chain to the root directory.  Placing your cursor someplace in an `index.md` file (I usually do this on the third like right below the top-level heading) the execute `form_index`.  This puts in a set of Markdown bullets with links back up through the hierarchy - kind of a road-map to get you back home.

_Note: use the sidebar (turn off/on with `ctrl-k-b` to see the wiki file structure as well. For me, this works well with the following two setting:_

```
"bold_folder_labels": true,
"preview_on_click": false, 
```

_(The second comes in particularly handy when using the `SideBarEnhancements` Package - otherwise anything you right-click on in the sidebar automatically gets previewed.  Having the preview setting disabled means that a double-click opens the file.)_

The `SideBarEnhancements` package has a great "open in app" feature that is really handy.  I found myself also wanting this feature within the Markdown text, so I wrote the `open_in_app` command.  Place the cursor on the file link, then hit the key-binding for `open_in_app` and the file pops open in the designated application.  See `OpenInApp.sublime-settings` for how to configure this: it takes some careful bookkeeping to keep the right file suffix lined up with the right application, but it's not too hard.   

<a name="key-bindings-2"></a>
### Key bindings

The three commands discussed above can be bound to keys to make them easier.  My key-bindings are:

```
{ "keys": ["ctrl+super+w", "o"], "command": "open_in_app" },
{ "keys": ["ctrl+super+w", "c"], "command": "toc_jump" },
{ "keys": ["ctrl+super+w", "i"], "command": "form_index" },
```

Think `"[o]pen"`, `"[c]enter"` on toc entry, and `"[i]ndex"`.

<a name="checking-the-indexmd-file"></a>
## Checking the index.md file

When you start dropping a lot of stuff into a namespace, it's easy to forget to tie it into the wiki text.  For me, this happens a lot with references such as papers and presentations, and a valuable reference can get lost in the fray because I haven't taken the time to enter some Markdown text to describe it and link to it.  Enter `index_check` - this looks for "widow" links (links in the Markdown that point to a file that doesn't seem to exist) and "orphans" (files in the current namespace directory that don't appear to be referenced).  If orphans are found, they are listed as links at the bottom of the buffer - these links can be cut/pasted into the appropriate location within the file.  

Check out `IndexCheck.sublime-settings` for settings on the check - generally this is just file types that you want to ignore in the check.

Because `index_check` is an every-once-in-a-while command, I haven't bothered to bind it to a key combination. so just open the `index.md` file for the intended namespace, and run the command from the command line using `view.run_command('index_check')`

<a name="tasks"></a>
## Tasks

I have implemented a really simple system for tracking tasks.  If you tag something in your markdown as `@task`, which I usually do at the beginning the a line, with descriptive text following:

```
@task - writeup the wiki commands
```

Then use `task_interface` to bring up a sorted list of tasks _from the current namespace down_.  So running this from the top level `index.md` will give all tasks from all projects, journals, etc..., and running it from the `index.md` file in a particular year namespace within the journal side of the wiki only finds the tasks associated with that year.

Note that the list of tasks is click-able, so you can go directly to the task definition.  I generally follow the task definition line with other descriptive text, or time-tagged entries of progress on the task.  Note that I've generated a time-tagging command `pop_date` that allows you to enter date, time or date/time strings in a few different styles directly into the text you are typing.

After a task is completed, change the `@task` to `@done` (and maybe enter some time-tagged text regarding its closure).  If a task is pending someone else's input, and you want to get it off of your radar screen, change the tag to `@pend`.

Note that the `task_interface` command lets you selected one of the three tags and generates the click-able list.  So you can quickly reference a completed task, or look at a list of pending tasks on which you are awaiting input from someone else.  

Because the `task_interface` and `pop_date` commands aren't specifically "wiki" items, I have them in a different key-binding structure:

```
{ "keys": ["ctrl+super+t"], "command": "task_interface" },
{ "keys": ["ctrl+alt+d"], "command": "pop_date" },
``` 

<a name="post-processing"></a>
## Post-processing

This pretty much wraps up my bunch of scripts required to maintain my wiki.  I generally work just in the Markdown, but sometimes it's helpful to have the wiki ported over to HTML.  This can be done on a case-by-case (file-by-file) basis using the `bash` script `panproc`.  Just giving `panproc` a markdown filename as the argument generates an HTML equivalent in the same directory. (Note that `panproc` assumes that `markdown.css` is available at `~/css/markdown.css`.)

The `panproc` script requires [pandoc][] to be installed, and assumes [sed][] is also resident.  

Note that I've structured `panproc` so that it can be called recursively - allowing an entire namespace (at a given level and everything below it) to be rendered in HTML.  So the entire wiki can be rendered by running the recursive call from the wiki root directory.  the recursive call is simply:

```
for i in $( find . -name "*.md" ); do panproc $i; done
```

<a name="summary"></a>
## Summary 

This pretty much wraps up my wiki system.  I use these scripts on Linux and Windows 7 every day, but there may be things about your system that conflict with these scripts.  I'm not very good at trouble-shooting beyond my systems - and I've barely learned just enough Python to write these scripts.  So... if you're having trouble let me know, but I can't make any promises.

- Kurt

<a name="release"></a>
## Release

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.


I'd really hate to see you lose anything valuable... I've done my best to make these scripts useful, but I make no claim regarding their correctness, and I cannot guarantee that using them will not result in data loss or mangling of some type.  Please use them only on data that you backup regularly, and know that I cannot be responsible for any loss of data you incur through the use of these scripts.

<a name="script-summary"></a>
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
[sed]: http://www.gnu.org/software/sed/