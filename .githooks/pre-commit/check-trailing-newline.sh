#!/bin/bash

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
    log_error "The following staged files have no trailing newline:"
    echo $no_newline
    exit 1
fi
