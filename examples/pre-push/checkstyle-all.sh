#!/bin/bash
 
# Run checkstyle before push
 
# This could also be a `post-commit` hook if you would rather fix style issues
# without a separate commit
 
./gradlew checkstyle
exit $?
