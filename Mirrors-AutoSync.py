
# Mirrors-AutoSync
# A tool to set schedules to rsync from remote server.
# developed by eastpiger from Geek Pie @ ShanghaiTech

#  - http://www.geekpie.org/
#  - http://www.eastpiger.com/
#  - https://github.com/ShanghaitechGeekPie/Mirrors-AutoSync

# ===========================================
config_file_dir = "/Mirrors-AutoSync/Mirrors-AutoSync.conf"
script_file_dir = "/Mirrors-AutoSync/script/"
# ===========================================

from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
import json
import datetime, time
import os

class task(object):
	"""scheduler task"""
	name = 'default'
	schedule = {}
	path = {}

	def __init__(self, name, schedule, exec, argument):
		super(task, self).__init__()

		self.name = name
		self.schedule = schedule
		self.exec = exec
		self.argument = argument

		self.schedule.setdefault('year', '*')
		self.schedule.setdefault('month', '*')
		self.schedule.setdefault('day', '*')
		self.schedule.setdefault('week', '*')
		self.schedule.setdefault('day_of_week', '*')
		self.schedule.setdefault('hour', '*')
		self.schedule.setdefault('minute', '*')
		self.schedule.setdefault('second', '*')

		print('	Load scheduler [' + self.name + '].')

	def runner(self):
		global method_lock
		global scheduler

		while method_lock > 1:
			print("	[{}] waiting.".format(self.name))
			time.sleep(10)

		method_lock += 1

		print("	[{}] running with [{}].".format(self.name, self.exec))

		statuscode = os.system("python3 {} {} {} {} > {}{}"
			.format(
				script_file_dir + self.exec,
				self.name,
				' '.join(self.argument),
				status_file_dir,
				log_file_dir,
				self.name)) >> 8

		print("	[{}] fired.".format(self.name, statuscode))

		if statuscode != 0:
			print("	[{}] script running with [{}] failed with error code {}."
				.format(self.name, self.exec, statuscode))
			if statuscode == 233:
				print("	[{}] script ask to retry after 10 minutes."
				scheduler.modify_job(
					self.name,
					next_run_time = datetime.datetime.now() + datetime.timedelta(seconds = 10*60),)

		method_lock -= 1

	def setup(self, scheduler):
		scheduler.add_job(
			self.runner,
			'cron',
			id = self.name,
			name = self.name,
			coalesce = True,
			misfire_grace_time = 86400,
			max_instances = 100,
			next_run_time = datetime.datetime.now(),
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

scheduler = BlockingScheduler(
	timezone = 'Asia/Shanghai',
)

config_file = open(config_file_dir, 'r')

content = json.loads(config_file.read())

log_file_dir = content['log_file_dir']
status_file_dir = content['status_file_dir']

method_lock = 0

for i in content['schedules']:
	t = task(i['name'], i['schedule'], i['exec'], i['argument'])
	t.setup(scheduler)

config_file.close()

print('	Finished.\n')

print('[Starting multithreading]\n')

try:
	scheduler.start()
except KeyboardInterrupt:
	pass

print('	Finished.\n')
