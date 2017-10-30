# This script does not follow the general command line argument convention.

import sys
import os

from writer import writer

Name			=	sys.argv[1]
ConfigPath		=	sys.argv[2]
StatusPath		=	sys.argv[3]
RemotePath		=	sys.argv[4]
LocalPath		=	sys.argv[5]
TimefilePath	=	sys.argv[6]

command_literal = "/Mirrors-AutoSync/script/quick-fedora-mirror -c /Mirrors-AutoSync/script/quick-fedora-mirror.conf --timefile {} --destination-dir {} --upstream {} {}".format(TimefilePath, LocalPath, RemotePath, "" if os.path.exists(TimefilePath) else "-a")

print("	[{}] run command {}.".format(Name, command_literal))

writer(Name, ConfigPath, StatusPath, -1)

statuscode = os.system(command_literal) >> 8

writer(Name, ConfigPath, StatusPath, statuscode)

if statuscode != 0:
	print("	[{}] failed with error code {}."
				.format(Name, statuscode))
	exit(233)
