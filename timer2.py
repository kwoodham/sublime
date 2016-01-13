#!/usr/bin/env python

import sys
import os
import time
import argparse

# Timer to support Pomodoro method (or other purposes)
# Kurt Woodham (kwoodham@gmail.com), 08 Jan 2016
# See: https://docs.python.org/3/howto/argparse.html
#
# usage: timer2.py [-h] [-d] [-u] count
#
# positional arguments:
#   count       number of minutes for counter (limit = 99)
#
# optional arguments:
#   -h, --help  show this help message and exit
#   -d, --down  count down
#   -u, --up    count up (default)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--down", help="count down", action="store_true")
parser.add_argument("-u", "--up", help="count up (default)", action="store_true")
parser.add_argument("count", help="number of minutes for counter (limit = 99)", type=int)
args = parser.parse_args()

# Check args (probably some way to do this automagically)
if (args.down and args.up):
    print("Use either --up or --down (not both). See -h")
    sys.exit()

# Have a 2 digit limit for output
if (args.count < 1) or (args.count > 99):
    print("Choose a duration in the range from 1 to 99 minutes. See -h")
    sys.exit()

# Set up as the default if neither set
if not(args.up or args.down):
    args.up = True

# Execute the timer up or down - format with \r end allows time
# left/accrued to be displayed on the same line.
print("Starting", args.count, "minute timer...")
for x in range(1, args.count):
    time.sleep(60)
    if args.up:
        print("  minutes past: {:2d}".format(x), end='\r')  # space for cursor at beginning of line
    elif args.down:
        print("  minutes left: {:2d}".format(args.count-x),  end='\r')
    else:
        print("something bad be happening: should not get here!")
        sys.exit()
time.sleep(60)

# Play the sound
if os.name == 'nt':
    import winsound
    print("\nTime!")
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
else:
    print("\nTime!", '\a')
