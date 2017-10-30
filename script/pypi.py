import sys
import os

from writer import writer

Name		=	sys.argv[1]
ConfigPath	=	sys.argv[2]
StatusPath	=	sys.argv[3]
RemotePath	=	sys.argv[4]
LocalPath	=	sys.argv[5]

print("	[{}] run command {}."
				.format(Name, "bandersnatch -c /Mirrors-AutoSync/bandersnatch.conf mirror 2>&1"))

writer(Name, ConfigPath, StatusPath, -1)

statuscode = os.system("bandersnatch -c /Mirrors-AutoSync/bandersnatch.conf mirror 2>&1"
	.format(LocalPath)) >> 8

writer(Name, ConfigPath, StatusPath, statuscode)

if statuscode != 0:
	print("	[{}] failed with error code {}."
				.format(Name, statuscode))
	exit(233)
