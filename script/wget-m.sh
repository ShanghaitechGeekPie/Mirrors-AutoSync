#!/bin/sh
# Wrapper around wget -m.
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

# TODO: Handle wget error and logs.

usage() {
    cat<<EOF
$0: Invalid argument(s)
Usage: $0 -u <url> -d <target> [-x <glob>] [--pre-release]
Wrapper around wget -m.
ARGUMENTS:
  -u,  --upstream=<url>         A url to the root of the site. No parent will be fetched.
  -d,  --target=<target>        The path to store the downloaded files locally. 
  -R,  --reject                 A comma separated list of file extensions to reject. Passed to wget -R unchanged.
  -x,  --remove                 A comma separated list of glob patterns to remove unwanted files, after wget -m finished.
                                Normally only used by the script itself.
       --pre-release            Fetch pre-releases. Default behavior is not fetch it. 
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
}

do_fetch() {
    wget -m "$UPSTREAM" -R "$EXCLUDE" -e "robots=off" -np -nH -E -P $TARGET
}

post_remove() {
    
    for pattern in ${REMOVE//,/ }
    do
        find $TARGET -name "$pattern" -type f | xargs -n1 -r -t rm
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
            -R|--reject)
                EXCLUDE=$2
                shift 2
                ;;
            -x|--remove)
                REMOVE=$2
                shift 2
                ;;
            *)
                usage
                ;;
        esac
    done
}

parse_arg $*

prepare
do_fetch
post_remove
