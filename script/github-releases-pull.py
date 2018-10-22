import sys
import os

from writer import writer

Name		=	sys.argv[1]
ConfigPath	=	sys.argv[2]
StatusPath	=	sys.argv[3]
RemotePath	=	sys.argv[4]
LocalPath	=	sys.argv[5]

command = "/Mirrors-AutoSync/script/github-releases-pull.sh -u {} -d {}".format(RemotePath, LocalPath)

print("	[{}] run command {}.".format(Name, command))

writer(Name, ConfigPath, StatusPath, -1)

statuscode = os.system(command) >> 8

writer(Name, ConfigPath, StatusPath, statuscode)

if statuscode != 0 and statuscode != 37:
	print("	[{}] failed with error code {}."
				.format(Name, statuscode))
	exit(233)
