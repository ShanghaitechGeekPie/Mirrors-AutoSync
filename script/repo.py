import sys
import os

from writer import writer

Name		=	sys.argv[1]
ConfigPath	=	sys.argv[2]
StatusPath	=	sys.argv[3]
RemotePath	=	sys.argv[4]
LocalPath	=	sys.argv[5]

print("	[{}] run command {}."
				.format(Name, "repo sync -d && repo forall -c 'git reset --hard' && repo forall -c 'git clean -f -d'"))
writer(Name, ConfigPath, StatusPath, -1)

statuscode = os.system("cd {} && repo sync -d && repo forall -c 'git reset --hard' && repo forall -c 'git clean -f -d'"
	.format(LocalPath)) >> 8

writer(Name, ConfigPath, StatusPath, statuscode)

if statuscode != 0:
	print("	[{}] failed with error code {}."
				.format(Name, statuscode))
	exit(233)
