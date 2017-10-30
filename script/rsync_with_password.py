import sys
import os

from writer import writer

Name		=	sys.argv[1]
ConfigPath	=	sys.argv[2]
StatusPath	=	sys.argv[3]
RemotePath	=	sys.argv[4]
LocalPath	=	sys.argv[5]

print("	[{}] run command {}."
				.format(Name, "RSYNC_PASSWORD=******** rsync -pPrtlvH --sparse --safe-links --delete --delete-delay --delay-updates --timeout=600 --contimeout=60 --progress {} {}\n".format(RemotePath, LocalPath)))

writer(Name, ConfigPath, StatusPath, -1)

statuscode = os.system("RSYNC_PASSWORD={} rsync -pPrtlvH --sparse --safe-links --delete --delete-delay --delay-updates --timeout=60 --contimeout=60 --progress {} {}"
	.format(os.getenv('PSW_' + Name), RemotePath, LocalPath)) >> 8

writer(Name, ConfigPath, StatusPath, statuscode)

if statuscode != 0:
	print("	[{}] failed with error code {}."
				.format(Name, statuscode))
	exit(233)
