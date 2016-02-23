
#Mirrors-AutoSync#

A tool to set schedules to rsync from remote server.

#Install#

> Docker

#Config

By default, config file directory is `/etc/Mirrors-AutoSync/Mirrors-AutoSync.conf`.

This is the basic structure of Mirrors-AutoSync.conf:
```JSON
{
	"output_file_dir" : "Mirrors-Status.json",
	"schedules" : [
		{
			"name" : "test1",
			"schedule" : {
				"second" : "*/2"
			},
			"path" : {
				"server" : "rsync://mirrors.example.com/",
				"remotepath" : "path/to/ubuntu",
				"localpath" : "/path/to/ubuntu"
			}
		},
		{
			"name" : "test2",
			"schedule" : {
				"second" : "*/3"
			},
			"path" : {
				"server" : "rsync://mirrors.example.com/",
				"remotepath" : "path/to/ubuntu",
				"localpath" : "/path/to/ubuntu"
			}
		},
		{
			"name" : "test3",
			"schedule" : {
				"second" : "*/5"
			},
			"path" : {
				"server" : "rsync://mirrors.example.com/",
				"remotepath" : "path/to/ubuntu",
				"localpath" : "/path/to/ubuntu"
			}
		}
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

#Information#

developed by eastpiger from Geek Pie @ ShanghaiTech

- [Github](https://github.com/ShanghaitechGeekPie/Mirrors-AutoSync)
- [Geek Pie Association @ ShanghaiTech University](http://www.geekpie.org/)
- [eastpiger](http://www.eastpiger.com/)
