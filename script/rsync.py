import sys
import json
import datetime, time
import os
import fcntl

Name		=	sys.argv[1]
RemotePath	=	sys.argv[2]
LocalPath	=	sys.argv[3]
StatusPath	=	sys.argv[4]

def writer(statuscode):
	if not os.path.exists(StatusPath):
		output_file = open(StatusPath, 'a+')
		output_file.close()

	output_file = open(StatusPath, 'r+')

	fcntl.flock(output_file.fileno(), fcntl.LOCK_EX)

	try:
		content = json.loads(output_file.read())
	except:
		content = []

	newstatus = {
		'name': Name,
		'statuscode': statuscode,
		'time': time.time()
	}

	insert = True
	for i in range(len(content)):
		if content[i]['name'] == Name:
			content[i] = newstatus
			insert = False
	if insert: content.append(newstatus)

	content = sorted(content, key = lambda t:t['name'])

	output_file.seek(0)

	output_file.write(json.dumps(content))

	output_file.truncate()

	output_file.close()

print("	[{}] run command {}."
				.format(Name, "rsync -rtlvH --safe-links --delete --delete-delay --delay-updates --timeout=600 --contimeout=60 --progress {} {}".format(RemotePath, LocalPath)))

writer(-1)

statuscode = os.system("rsync -rtlvH --safe-links --delete --delete-delay --delay-updates {} {}"
	.format(RemotePath, LocalPath)) >> 8

writer(statuscode)

if statuscode != 0:
	print("	[{}] failed with error code {}."
				.format(Name, statuscode))
	exit(233)
