
# Mirrors-AutoSync #

A tool to set schedules to rsync from remote server.

# Install #

> Docker

# Config

By default, config file directory is `/etc/Mirrors-AutoSync/Mirrors-AutoSync.conf`.

This is the basic structure of Mirrors-AutoSync.conf:
```JSON
{
	"base_dir" : "/mirrors/",
	"status_file_dir" : "/mirrors/Mirrors-Status.json",
	"log_file_dir" : "/mirrors/logs/",
	"schedules" : [
		{
			"name" : "aosc",
			"schedule" : {
				"hour" : "1",
				"minute": 0,
				"second": 0
			},
			"exec" : "rsync.py",
			"argument" : [
				"rsync://mirrors.yun-idc.com/anthon",
				"/mirrors/aosc"
			]
		},
		{
			"name" : "archlinux",
			"schedule" : {
				"hour" : "0,8,16",
				"minute": 0,
				"second": 0
			},
			"exec" : "rsync.py",
			"argument" : [
				"rsync://mirrors.tuna.tsinghua.edu.cn/archlinux",
				"/mirrors/archlinux"
			]
		},
	]
}

```

The schedule accept these:

 - year
 - month
 - day
 - week
 - day_of_week
 - hour
 - minute
 - second

and can be under this expression:

```
Expression	Field	Description
*			any		Fire on every value
*/a			any		Fire every a values, starting from the minimum
a-b			any		Fire on any value within the a-b range (a must be smaller than b)
a-b/c		any		Fire every c values within the a-b range
xth y		day		Fire on the x -th occurrence of weekday y within the month
last x		day		Fire on the last occurrence of weekday x within the month
last		day		Fire on the last day within the month
x,y,z		any		Fire on any matching expression; can combine any number of any of the above expressions
```

You can use different sync method under folder script. Assign different script by changing the option exec and argument

# Information #

developed by eastpiger from Geek Pie @ ShanghaiTech

- [Github](https://github.com/ShanghaitechGeekPie/Mirrors-AutoSync)
- [Geek Pie Association @ ShanghaiTech University](http://www.geekpie.org/)
- [eastpiger](http://www.eastpiger.com/)
