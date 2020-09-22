import os
import re
from string import Template
import tempfile
import shutil
import datetime
import json

# 14 May 2019
# Add in ability to handle priorities - note that it looks like priorities
# are removed from completed tasks, so I only need to process if the task
# is open

# 14 May 2019
# Added in sorting - priorities come first, then sort by staleness - need to 
# do this in two steps because the `reverse=True` should only be on the staleness

# 26 Apr 2019
# Add in context for lines that have it - wanted for "summary" board that 
# puts meta-project (GPX2, D209) in as context.
# Process tasks that don't have a project identifier

# 24 Apr 2019
# Firefox doesn't like full path for stylesheet - so change to relative path.
# Also changed path styles in JSON to "/c/Users/..." style (what python likes)


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
styleSheet = os.path.relpath(data['styleSheet'],os.getcwd())


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
priPattern = re.compile("\([A-D]\)")
projPattern = re.compile(" \+[a-zA-Z0-9]+")
statePattern = re.compile(" s\:[a-zA-Z0-9]+")
contextPattern = re.compile(" \@[a-zA-Z0-9]+")

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
        datec = datePattern.findall(line)[0] # Date closed
        line = line[(len(datec)+1):]
    
    # Now the rest of the tasks (as well as completed
    # tasks that haven't been full parsed
    pri = priPattern.findall(line)
    if pri == []:
        pri = '-' 
    else:
        pri = pri[0]
        line = line[(len(pri)+1):]
    dateo = datePattern.findall(line)[0] # Date opened
    line = line[(len(dateo)+1):]

    # 26 Apr 2019 if there is a project it will provide
    # the separation between the task text and any tags
    # If there isn't a project, treat the whole line as 
    # the task as well as the source for any tags
    if line.find(' +') != (-1):
        proj = projPattern.findall(line)[0].lstrip()
        [task, tags] = projPattern.split(line)
    else:
        proj = ''
        task = line
        tags = line

    # If processed in Sublime it has an "s:" tag and we
    # can pull the state out of the tags. Otherwise
    # it was closed outside of Sublime (as processed
    # above) or it is unassigned.
    if tags.find(' s:')!=(-1):
        state = statePattern.findall(tags)[0].lstrip(' s:')
    elif state=='':
        state = 'unassigned'

    # 26 Apr 2019 Extract context if it's present
    if tags.find(' @')!=(-1):
        context = contextPattern.findall(tags)[0].lstrip()
    else:
        context = ''

    # Generate "staleness" or days it took to complete
    date1 = dateo.split('-')
    date1 = datetime.date(int(date1[0]),int(date1[1]),int(date1[2]))
    if state== closedState:
        date2 = datec.split('-')
        date2 = datetime.date(int(date2[0]),int(date2[1]),int(date2[2]))
    else:
        date2 = datetime.date.today()  
    days = (date2-date1).days # 14 May 2019 - leave this non-string to support sorting

    taskArray.append({'pri': pri, 'task': task, 'project': proj, 'context': context, 
        'state': state, 'startDate': dateo, 'endDate': datec, 'days': days})


# Sort the task list with high priority first, followed by age
taskArray = sorted(taskArray, key = lambda i: i['days'], reverse=True)
taskArray = sorted(taskArray, key = lambda i: i['pri'])


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
