#!/usr/bin/env python

import sys
import os
import time

print("Starting", sys.argv[1], "minute timer...")
for x in range(1, int(sys.argv[1])):
    time.sleep(60)
    print(x, "minute(s) past...")
time.sleep(60)
if os.name == 'nt':
    import winsound
    print("Time!")
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
else:
    print("Time!", '\a')
