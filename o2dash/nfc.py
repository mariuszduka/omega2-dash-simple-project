import time
import json
import os
from os import path

#
# Check acceptable access cards
#
def checkUID(wait = 5):	
	nfc_list = '/usr/bin/nfc-list'
	
	# Check if nfc-list is availale
	if not path.exists(nfc_list):
		return False
		
	# Acceptable access cards
	file_uids = 'access.json'
	if path.exists(file_uids):
		f = open(file_uids)
		acceptedUids = json.load(f)
		f.close()
	else:
		return False
	
	file_nfc_uid = '/root/nfc.txt'
	
	start = time.time()
	access = False
	
	while time.time() < start + wait:
		cmd = nfc_list + " | grep UID | sed -e 's/ //g' -e 's/^.*://' > " + file_nfc_uid
		os.system(cmd)
		
		uid = ""
		
		if path.exists(file_nfc_uid):
			f = open(file_nfc_uid)
			uid = f.read()
			f.close()

		uid = uid.rstrip('\n')
		# print(uid)

		for acceptedUid in acceptedUids['uids']:
			if(acceptedUid == uid):
				print("Access!")
				access = True
				break
		
		if (access == True):
			break

	if path.exists(file_nfc_uid):
		os.remove(file_nfc_uid)
		
	return access