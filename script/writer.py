import json
import datetime, time
import os
import fcntl

def get_info(Name, ConfigPath):
	config_file = open(ConfigPath, 'r')
	content = json.loads(config_file.read())
	schedules = [i for i in content['schedules'] if (i['name'] == Name)]
	if len(schedules) > 0:
		schedules = schedules[0]
	else:
		schedules = None
	if schedules:
		ret = {
			'schedule': schedules['schedule']
				if ('schedule' in schedules)
				else [],
			'upstream': schedules['upstream']
				if ('upstream' in schedules)
				else (schedules['schedule']['argument'][0]
					if (
						('schedule' in schedules) and
						('argument' in schedules['schedule']) and
						(len(schedules['schedule']['argument']) > 0))
					else None),
		}
		return ret;
	else:
		return None;

def writer(Name, ConfigPath, StatusPath, statuscode):
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
		'lastsuccess': time.time()
			if (statuscode == 0)
			else(content['lastsuccess']
				if ('lastsuccess' in content)
				else 0
			),
		'time': time.time(),
		'info': get_info(Name, ConfigPath)
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
