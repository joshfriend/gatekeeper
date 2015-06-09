#!/bin/bash

# Only scan changed/added files
staged=$(git diff --staged --name-status | grep '[MA]' | awk '{ print $2 }')

ignorepattern="(.*\.json)"

text_files=()
for file in $staged; do
    # Check if file is text
    ftype=$(file $file)
    if ! [[ "$ftype" =~ "text" ]]; then
        continue
    fi

    if [[ "$file" =~ $ignorepattern ]]; then
        continue
    fi

    text_files+=($file)
done

have_trailing_space=$(egrep -l " +$" $text_files)

if [ "$have_trailing_space" ]; then
    log_error "The following staged files have trailing whitespace:"
    echo $have_trailing_space
    exit 1
fi
