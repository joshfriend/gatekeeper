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

RED='\033[0;31m'
YELLOW='\033[0;33m'
WHITE='\033[0;37m'
BOLD='\033[0;1m'
UNDERLINE='\033[0;4m'
BLINK='\033[0;5m'
NC='\033[0m' # No Color

# Logging helpers
_log_message() {
    text=$1
    shift
    if [ -z "$TERM" ]; then
        printf "$text\n"
    else
        printf "$@$text${NC}\n"
    fi
}
export -f _log_message

log_info() {
    _log_message "$1" ${WHITE}
}
export -f log_info

log_warn() {
    _log_message "$1" ${YELLOW}
}
export -f log_warn

log_error() {
    _log_message "$1" ${RED}
}
export -f log_error


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
