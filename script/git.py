import sys
import os

from writer import writer

Name		=	sys.argv[1]
ConfigPath	=	sys.argv[2]
StatusPath	=	sys.argv[3]
RemotePath	=	sys.argv[4]
LocalPath	=	sys.argv[5]

print("	[{}] run command {}."
				.format(Name, "git fetch origin master -v --progress --tags && git update-server-info"))

writer(Name, ConfigPath, StatusPath, -1)

statuscode = os.system("cd {} && git fetch origin master -v --progress --tags && git update-server-info"
	.format(LocalPath)) >> 8

writer(Name, ConfigPath, StatusPath, statuscode)

if statuscode != 0:
	print("	[{}] failed with error code {}."
				.format(Name, statuscode))
	exit(233)
