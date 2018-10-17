#!/bin/bash
# Bash script to sync releases of a particular GitHub repository.
# WILL NOT DOWNLOAD SOURCE TAR BALLS
# WILL NOT PRUNE ALREADY DOWNLOADED RELEASES WHICH LATER GET DELETED IN REPO
#
# Copyright (C) 2018 Jinrui Wang <wangjr@shanghaitech.edu.cn>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, version 3.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# TODO: Handle wget errors better
# TODO: Prune removed releases
# TODO: Provide switch whether fetch source tar balls
# TODO: Provide download statistics

usage() {
	cat<<EOF
$0: Invalid argument(s)
Usage: $0 -u <owner/repo> -d <target> [--locked] [--pre-release]
Bash script to sync releases of a particular GitHub repository.

ARGUMENTS:
  -u,  --upstream=<owner/repo>  A string to indicate which repo to pull. 
  -d,  --target=<target>        The path to store the downloaded files locally. 
       --locked                 Passing in anything indicate the lock is acquired. 
                                Normally only used by the script itself.
       --pre-release            Fetch pre-releases. Default behavior is not fetch it. 

NOTICE:
     1. I would strongly oppose any action to parallelize the download, to prevent flooding GitHub servers, even if this is extremely unlikely.
     2. WILL NOT DOWNLOAD SOURCE TAR BALLS.
     3. WILL NOT PRUNE ALREADY DOWNLOADED RELEASES WHICH LATER GET DELETED IN REPO.

LICENSING
     Licensed under AGPL v3.0.

AUTHOR
    Jinrui Wang <wangjr@shanghaitech.edu.cn>
EOF
	exit 1
}

prepare() {
	mkdir -p $TARGET
	if [ $? -ne 0 ] ; then
		echo "$0: Unable to create directories. Refer to above for error details. Aborting!"
		exit 1
	fi

	touch $LOCK_FILE
	if [ $? -ne 0 ] ; then
		echo "$0: Unable to write to lock file. Refer to above for error details. Aborting!"
		exit 1
	fi
}

fetch_page_content() {
	if [ -n "$PRE_RELEASE" ] ; then 
		grep "https://github.com/$2/releases/download/[^\"]+" $1 | xargs -r -n1 -t wget -nc
	else 
		grep "https://github.com/$2/releases/download/[^\"]+|((?<=prerelease\": )((true)|(false)))" -oP $1 \
			| awk 'BEGIN{p=1}{if($1=="true"){p=0}else if($1=="false"){p=1}else if(p==1){print $1}}' \
			| xargs -r -n1 -t wget -nc
	fi
}

do_fetch() {
	cd $TARGET

	wget --save-headers https://api.github.com/repos/$UPSTREAM/releases -O $tempfile
	
	if [ $? -ne 0 ] ; then
		echo "$0: Repository not found or GitHub unreachable!"
		exit 1
	fi
	
	fetch_page_content $tempfile $UPSTREAM

	while [ -n "$(grep -o rel=\"next\" $tempfile)" ] ; do
		grep -oP "https://api.github.com/repositories/\\d+/releases\\?page=\\d+(?=>; rel=\"next\")" $tempfile | xargs wget --save-headers -O $tempfile 
		fetch_page_content $tempfile $UPSTREAM
		
		while [ $? -ne 0 ] ; do
			echo "$0: Retrying download after 5 seconds!"
			sleep 5
			echo "$0: Retrying!"
			fetch_page_content $tempfile $UPSTREAM
		done
	done
}

parse_arg() {
	while [ $# -gt 0 ] ; do
		case $1 in
			-u|--upstream)
				UPSTREAM=$2
				shift 2
				;;
			-d|--target)
				TARGET=$2
				shift 2
				;;
			--locked)
				LOCKED=1
				shift 1
				;;
			--pre-release)
				PRE_RELEASE=1
				shift 1
				;;
			*)
				usage
				;;
		esac
	done
}

parse_arg $*

LOCK_FILE=$TARGET/.github-releases-pull.${UPSTREAM//\//@}.lock

if [ -n "$UPSTREAM" ] && [ -n "$TARGET" ] ; then
	if [ -n "$LOCKED" ] ; then
		tempfile=`mktemp -p "" github-releases-pull.index.XXXXXX` && { do_fetch; }
	else
		prepare
		flock -E233 -n "$LOCK_FILE" -c "$0 $* --locked"
		ret=$?
		if [ $ret -eq 233 ] ; then
			echo "$0: Lock contention. Aborting!"
			exit 37
		elif [ $ret -ne 0 ] ; then 
			exit $ret
		else
			exit 0
		fi
	fi
else 
	usage
fi

