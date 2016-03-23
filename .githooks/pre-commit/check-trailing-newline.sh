#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

# Only scan changed/added files
staged=$(git diff --staged --name-status | grep '[MA]' | awk '{ print $2 }')

ignorepattern="(.*\.json)"

no_newline=()
for file in $staged; do
    # Check if file is text
    ftype=$(file $file)
    if ! [[ "$ftype" =~ "text" ]]; then
        continue
    fi

    if [[ "$file" =~ $ignorepattern ]]; then
        continue
    fi

    # http://backreference.org/2010/05/23/sanitizing-files-with-no-trailing-newline/
    tail -c1 $file | read -r _
    if [ $? -ne 0 ]; then
        no_newline+=($file)
    fi
done

if [ "$no_newline" ]; then
    printf "${RED}The following staged files have no trailing newline:${NC}\n"
    echo $no_newline
    exit 1
fi
