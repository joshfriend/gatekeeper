#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

# Only scan changed/added files
staged=$(git diff --staged --name-status | grep '[MA]' | awk '{ print $2 }')

text_files=()
for file in $staged; do
    # Check if file is text
    ftype=$(file $file)
    if ! [[ "$ftype" =~ "text" ]]; then
        continue
    fi
    text_files+=($file)
done

have_trailing_space=$(egrep -l " +$" $text_files)

if [ "$have_trailing_space" ]; then
    printf "${RED}The following staged files have trailing whitespace:${NC}\n"
    echo $have_trailing_space
    exit 1
fi
