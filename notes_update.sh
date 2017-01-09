#!/bin/bash

cd ~/work-notes/
python ./changed_files.py
while read -r line; do pynproc.py --input $line; done < db.files


