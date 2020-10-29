import time
from interface import *
from remote import *

autoRefresh = True

print("Starting system...")
# Initalize user interface
(lv, scr) = mainWindow()

# Load the screen
lv.scr_load(scr)

# Threading
if autoRefresh:
	import _thread

	interval = 30

	def monitor(name):
	    while True:
	    	if autoRefresh == True:
	    		refreshRemote()
	    	time.sleep(interval)
	
	_thread.start_new_thread(monitor, (0, ))
else:
	refreshRemote()

while True:
	pass