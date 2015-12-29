
# Mirrors-AutoSync
# A tool to set schedules to rsync from remote server.
# developed by eastpiger from Geek Pie @ ShanghaiTech

#  - http://www.geekpie.org/
#  - http://www.eastpiger.com/
#  - https://github.com/ShanghaitechGeekPie/Mirrors-AutoSync

# ===========================================
config_file_dir = "/Mirrors-AutoSync/Mirrors-AutoSync.conf"
# ===========================================

from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
import json
import time
import os

class task(object):
	"""scheduler task"""
	name = 'default'
	schedule = {}
	path = {}

	def __init__(self, name, schedule, path):
		super(task, self).__init__()

		self.name = name
		self.schedule = schedule
		self.path = path

		self.schedule.setdefault('year', '*')
		self.schedule.setdefault('month', '*')
		self.schedule.setdefault('day', '*')
		self.schedule.setdefault('week', '*')
		self.schedule.setdefault('day_of_week', '*')
		self.schedule.setdefault('hour', '*')
		self.schedule.setdefault('minute', '*')
		self.schedule.setdefault('second', '*')
		self.path.setdefault('server', 'rsync://mirrors.ustc.edu.cn/')
		self.path.setdefault('remotepath', 'ubuntu')
		self.path.setdefault('localpath', '/data/www/mirrors/ubuntu')

		print('	Load scheduler ' + self.name + '.')

	def writer(self, statuscode):
		global filelock

		while filelock : time.sleep(0.1)

		filelock = True

		output_file = open(status_file_dir, 'a+')
		output_file.close()

		output_file = open(status_file_dir, 'r')

		try:
			content = json.loads(output_file.read())
		except:
			content = []

		output_file.close()

		output_file = open(status_file_dir, 'w')

		newstatus = {
			'name': self.name,
			'statuscode': statuscode,
			'upstream': self.path['server'] + self.path['remotepath'],
			'path': self.path['localpath'],
			'time': time.time()
		}

		insert = True
		for i in range(len(content)):
			if content[i]['name'] == self.name:
				content[i] = newstatus
				insert = False
		if insert: content.append(newstatus)

		content = sorted(content, key = lambda t:t['name'])

		output_file.write(json.dumps(content))

		output_file.close()

		filelock = False

	def runner(self):
		global rsynclock

		while rsynclock >= 1 :
			print("	[{}] other job is running, wait for 5 minutes.\n".format(self.name))
			time.sleep(300)

		rsynclock += 1

		print("	[{}] running with [rsync -Par {}{} {}].\n".format(self.name, self.path['server'], self.path['remotepath'], self.path['localpath']))

		self.writer(-1)

		statuscode = os.system("rsync -Par {}{} {}{} > {}".format(self.path['server'], self.path['remotepath'], base_dir, self.path['localpath'], log_file_dir)) >> 8

		print("	[{}] finished with exit code {}.\n".format(self.name, statuscode))

		self.writer(statuscode)

		rsynclock -= 1

	def setup(self, scheduler):
		scheduler.add_job(
			self.runner,
			'cron',
			name = self.name,
			max_instances = 100,
			#next_run_time = None,
			year = self.schedule['year'],
			month = self.schedule['month'],
			day = self.schedule['day'],
			week = self.schedule['week'],
			day_of_week = self.schedule['day_of_week'],
			hour = self.schedule['hour'],
			minute = self.schedule['minute'],
			second = self.schedule['second'],
		)

		print('	Set scheduler ' + self.name + '.')

print('''
===========================================================

                    Mirrors-AutoSync

  A tool to set schedules to rsync from remote server.
  developed by eastpiger from Geek Pie @ ShanghaiTech

                - http://www.geekpie.org/
                - http://www.eastpiger.com/
 - https://github.com/ShanghaitechGeekPie/Mirrors-AutoSync

===========================================================
''')

print('[Loading config file]\n')

scheduler = BlockingScheduler()

config_file = open(config_file_dir, 'r')

content = json.loads(config_file.read())

base_dir = content['base_dir']
status_file_dir = content['status_file_dir']
log_file_dir = content['log_file_dir']

for i in content['schedules']:
	t = task(i['name'], i['schedule'], i['path'])
	t.setup(scheduler)

config_file.close()

print('	Finished.\n')

print('[Seting up multithreading locks]\n')

filelock = False
rsynclock = 0

print('	Finished.\n')

print('[Starting multithreading locks]\n')

try:
	scheduler.start()
except KeyboardInterrupt:
	pass

print('	Finished.\n')
