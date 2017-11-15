#!/bin/bash
if [ -e "db.files" ]  
then
	cp -f db.files db.files.bak
fi
if [ -e "db.pickle" ]  
then
	cp -f db.pickle db.pickle.bak
fi
python3 ./changed_files.py
while read -r line; do python3 ~/.local/bin/pynproc.py --input $line; done < db.files
