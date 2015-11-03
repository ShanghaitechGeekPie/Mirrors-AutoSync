from distutils.core import setup
setup(
	name = 'Mirrors-AutoSync',
	description = 'A tool to set schedules to rsync from remote server.',
	author = 'eastpiger',
	author_email = 'eastpiger@gmail.com',
	url = 'https://github.com/ShanghaitechGeekPie/Mirrors-AutoSync',
	requires = ['apscheduler'],
	version = '1.0.0',
	py_modules = ['Mirrors-AutoSync'],
)
