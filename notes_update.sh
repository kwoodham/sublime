#!/bin/bash

cd ~/work-notes/
python3 ./changed_files.py
while read -r line; do python3 ~/.local/bin/pynproc.py --input $line; done < db.files
