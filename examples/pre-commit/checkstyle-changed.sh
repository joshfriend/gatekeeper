#!/bin/bash

# Run checkstyle on changed files

CHANGED_FILES=$(git diff --staged --name-status | grep '[MA].*\.java' | awk '{ print $2 }')
if [ "$CHANGED_FILES" ]; then
    checkstyle -c app/config/checkstyle/checkstyle.xml $CHANGED_FILES
    exit $?
fi
