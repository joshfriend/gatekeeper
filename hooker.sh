#!/bin/bash

dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
this=$dir/`basename "${BASH_SOURCE[0]}"`

# http://git-scm.com/docs/githooks
hook_names="
applypatch-msg     \
commit-msg         \
post-update        \
pre-applypatch     \
pre-commit         \
pre-push           \
pre-rebase         \
prepare-commit-msg \
update             \
"

if [ "$1" = "--install" ]; then
    echo "Hooking you up..."
    for hook in $hook_names; do
        ln -sf $this .git/hooks/$hook
    done
else
    hook_name=$(basename "$this")
    hook_dir="$dir/../../.hooks/$hook_name"
    hook_files=$(find $hook_dir -perm +111 -type f 2> /dev/null)

    for hook in $hook_files; do
        $hook $* || exit $?
    done
fi
