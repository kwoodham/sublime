# sublime

## Introduction

This repository maintains a set of [Sublime Text 3][st3] (hereafter: ST3) scripts that I have developed to manage my personal workflow, using the [ST3 API][api].  The dominant theme here is to set up a "wiki" flavor that allows me to create and capture links between documents and headers (in the same document or other documents).  Additionally, I handle tasks within my pages (outstanding, pending, and done).

All wiki pages are in [Markdown][md]

The "journal" portion of my wiki has one page per week, with day headers pre-populated for each day.  There are a couple scripts for configuring a year's index page, and initializing a week page.

The wiki can be generated and traversed standalone - or it can be rendered into html for local display or pushing to a web server.  I use a `bash` script that wraps a little `sed` around [pandoc][] for rendering.   

## Wiki Configuration

I am in favor of using a file system hierarchy for a wiki rather than a "flat" directory.  This helps me keep the number of files in a directory reasonable, and I don't have to worry about clobbering a file with an identically-named file related to a different topic.  The configuration that has evovled for me is to have an `index.md` file in each directory that provides an anchor for that topic.  I developed a script to populate the index file with links to navigate on up the wiki to the root, and another script that will check that all the links in the file are valid (point to a real location) and that all files in the directory are referenced within the index.

## Script summary

| Script                        | Purpose                                                    |
| ----------------------------- | ---------------------------------------------------------- |
| `new_year.py`                 | Generate a year index file with links to each week         |
| `wiki_template.py`            | Populate a week's page with day headers, etc...            |
| `form_index.py`               | Paste in a road-map to navigate back up the wiki structure |
| `index_check.py`              | Check for bad links, widows (missing links), and           |
|                               | orphans (unreferenced files)                               |
| `IndexCheck.sublime-settings` | Configuration file for index check                         |
| `OpenInApp.sublime-settings`  | purpose                                                    |
| `link_to_heading.py`          | purpose                                                    |
| `open_in_app.py`              | purpose                                                    |
| `open_link_under_cursor.py`   | purpose                                                    |
| `paste_wiki_link.py`          | purpose                                                    |
| `pop_date.py`                 | purpose                                                    |
| `show_instances.py`           | purpose                                                    |
| `slugify.py`                  | purpose                                                    |
| `task_interface.py`           | purpose                                                    |


[st3]: http://www.sublimetext.com/3
[api]: http://www.sublimetext.com/docs/3/api_reference.html
[md]: http://daringfireball.net/projects/markdown/syntax
[pandoc]: http://johnmacfarlane.net/pandoc/
