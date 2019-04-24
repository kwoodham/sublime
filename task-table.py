import os
import re
from string import Template
import tempfile
import shutil
import datetime
import json

# 24 Apr 2019
# Firefox doesn't like "c:\Users\..." path for stylesheet
# change to relative path

# 22 Apr 2019
# Load in specific settings through JSON

# 18 Apr 2019
# Added in "staleness" display for aging tasks

# 17 Apr 2019
# Kurt Woodham
# Creates a Kanban page for todo.txt tasks. 
# Needs the .css file and the two template files in the current
# directory.

with open('task-table.json') as config_file:
    data = json.load(config_file)


filename = data['filename']
stateArray = data['stateArray']
closedState = data['closedState']
taskTableOpen = data['taskTableOpen']
taskTableClosed = data['taskTableClosed']
pageTitle = data['pageTitle']
styleSheet = data['styleSheet']

# 24 Apr 2019 - change stylesheet to relative path
styleSheet = styleSheet.replace("\\", "/")
styleSheet = styleSheet.replace("C:","/c")
styleSheet = os.path.relpath(styleSheet,os.getcwd())


# Width of each column as a percent:
colWidth = str(int(100/len(stateArray)))

# Read in the tasks
f = open(filename,"r")
s = f.read()
f.close()

# Read in the template
f = open( taskTableOpen )
srcOpen = Template( f.read() )
f.close()

f = open( taskTableClosed)
srcClosed = Template( f.read() )
f.close()

# Some patterns used in searches
datePattern = re.compile("[0-9-]+")
projPattern = re.compile(" \+[a-zA-Z0-9]+")

## tempfile for creating output
f, abs_path = tempfile.mkstemp()
new_file = open(f, 'w', encoding="utf-8")

# Dictionary object containing the tasks
taskArray = []

# Parse out the individual tasks and process
tasks = s.splitlines()
for line in tasks:
    state = ''
    datec = ''

    # First handle completed tasks - some of which
    # may have been worked outside of Sublime, so
    # they won't have a closed state appended.
    # Pull off the leading "x" and completion date
    if line[0:2]=='x ':
        state = closedState
        line = line[2:]
        datec = datePattern.findall(line)[0]
        line = line[(len(datec)+1):]
    
    # Now the rest of the tasks (as well as completed
    # tasks that haven't been full parsed
    dateo = datePattern.findall(line)[0]
    line = line[(len(dateo)+1):]

    # This will barf if there is no project assigned
    # No error checking here.
    proj = projPattern.findall(line)[0].lstrip()
    [task, tags] = projPattern.split(line)

    # If processed in Sublime it has an "s:" tag and we
    # can pull the state out of the tags. Otherwise
    # it was close outside of Sublime (as processed
    # above) or it is unassigned.
    if tags.find('s:')!=(-1):
        state = tags[(tags.find("s:")+2):]
    elif state=='':
        state = 'unassigned'

    # Generate "staleness" or days it took to complete
    date1 = dateo.split('-')
    date1 = datetime.date(int(date1[0]),int(date1[1]),int(date1[2]))
    if state== closedState:
        date2 = datec.split('-')
        date2 = datetime.date(int(date2[0]),int(date2[1]),int(date2[2]))
    else:
        date2 = datetime.date.today()  
    days = '(' + str( (date2-date1).days ) + ')'

    taskArray.append({'task': task, 'project': proj, 'state': state,
        'startDate': dateo, 'endDate': datec, 'days': days})

## Set up the HTML preamble
new_file.write('<!DOCTYPE html>\n')
new_file.write('<html>\n')
new_file.write('<head>\n')
new_file.write('<title>' + pageTitle + '</title>\n')
new_file.write('<link rel="stylesheet" href="' + styleSheet + '">\n')
new_file.write('</head>\n')
new_file.write('<body>\n')
new_file.write('<h1>' + pageTitle + '</h1>\n')
new_file.write('<table>\n')
new_file.write('<tr>\n')

## Loop through each state as a column in the task table. Each
# column is a table that contains a header in the first row, followed
# rows of task tables - using the templates defined in external files
# for open and closed entries.
for state in stateArray:

    new_file.write('<td style="width:' + colWidth + '%">\n')
    new_file.write('<table style="width: 100%">\n') # use the whole column
    new_file.write('<tr><th>' + state + '</th></tr>\n')

    for i in range(len(taskArray)):
    
        if taskArray[i]['state']==state:
            if state== closedState:
                result = srcClosed.substitute(taskArray[i])
            else:
                result = srcOpen.substitute(taskArray[i])
    
            for line in result:
                new_file.write(line)

    # Close out the column tags
    new_file.write('</table>\n')
    new_file.write('</td>\n')

# Close out the entire task table and file tags
new_file.write('</tr>\n')
new_file.write('</table>\n')
new_file.write('</body>\n')
new_file.write('</html>')

# copy out to task page
new_file.close()
os.remove(filename.replace('txt','html'))
shutil.move(abs_path,filename.replace('txt','html'))
