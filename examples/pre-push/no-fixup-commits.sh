#!/bin/bash

# This hoook will prevent pushing fixup commits without rebasing them away.

remote="$1"
url="$2"

z40=0000000000000000000000000000000000000000

while read local_ref local_sha remote_ref remote_sha; do
    if [ "$local_sha" = $z40 ]; then
        # Handle delete
        :
    else
        if [ "$remote_sha" = $z40 ]; then
            # New branch, examine all commits
            range="$local_sha"
        else
            # Update to existing branch, examine new commits
            range="$remote_sha..$local_sha"
        fi

        # Check for WIP commit
        commit=`git rev-list -n 1 --grep '^fixup!' "$range"`
        if [ -n "$commit" ]; then
            log_error "$local_ref contains fixup commits."
            log_warn "Please use rebase to autosquash these commits before pushing."
            exit 1
        fi
    fi
done

exit 0
