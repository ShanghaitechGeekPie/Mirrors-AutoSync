
#Mirrors-AutoSync#

A tool to set schedules to rsync from remote server.

#Install#

> python3 setup.py install

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

#Information@

developed by eastpiger from Geek Pie @ ShanghaiTech

- [Github](https://github.com/ShanghaitechGeekPie/Mirrors-AutoSync)
- [Geek Pie Association @ ShanghaiTech University](http://www.geekpie.org/)
- [eastpiger](http://www.eastpiger.com/)
