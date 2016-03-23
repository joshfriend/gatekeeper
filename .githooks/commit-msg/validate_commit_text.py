#!/usr/bin/env python
#
# A commit hook to validate commit messages based on the rules in this article:
#  http://chris.beams.io/posts/git-commit/

import re
import os
import sys
import string
import textwrap
from functools import wraps

if os.getenv('TERM'):
    colors = True
else:
    colors = False


class TermColors:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'

    FG_BLACK = '\033[30m'
    FG_RED = '\033[31m'
    FG_GREEN = '\033[32m'
    FG_YELLOW = '\033[33m'
    FG_BLUE = '\033[34m'
    FG_MAGENTA = '\033[35m'
    FG_CYAN = '\033[36m'
    FG_WHITE = '\033[37m'

    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


MAX_SUBJECT_LENGTH = 50
MAX_BODY_WIDTH = 72


def _log(text, *options):
    if colors:
        print(''.join(options) + text + TermColors.ENDC)
    else:
        print(text)


def fail(msg):
    _log(msg, TermColors.BOLD, TermColors.FG_RED)


def warn(msg):
    _log(msg, TermColors.FG_YELLOW)


def info(msg):
    _log(msg, TermColors.FG_WHITE)


def run_order(order):
    def wrap(func):
        func._order = order
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return wrap


@run_order(1)
def test_subject_line_is_capitalized(msg):
    subject = msg.split('\n')[0].strip()
    if subject.startswith('fixup!'):
        # ignore rule for `commit --fixup`
        return msg
    if not subject[0].isupper():
        fail('Subject line should be capitalized')
        return None
    return msg


@run_order(1)
def test_subject_length_limit(msg):
    subject = msg.split('\n')[0].strip()
    if len(subject) > MAX_SUBJECT_LENGTH:
        fail('Subject should be less than %i characters' % MAX_SUBJECT_LENGTH)
        return None
    return msg


@run_order(1)
def test_subject_doesnt_end_with_period(msg):
    subject = msg.split('\n')[0].strip()
    if subject.endswith('.'):
        fail('Subject should not end with a period')
        return None
    return msg


@run_order(1)
def test_blank_line_after_subject(msg):
    lines = map(string.strip, msg.split('\n'))
    # Remove ignored lines from message
    lines = filter(lambda x: not x.startswith('#'), lines)
    if len(lines) > 1 and lines[1]:
        fail('Separate subject from body with a blank line')
        return None
    return msg


@run_order(1)
def test_subject_does_not_contain_issue_key(msg):
    subject = msg.split('\n')[0].strip()
    issue_id_re = re.compile(r'[A-Z]+-\d+')
    if issue_id_re.match(subject):
        fail('Subject should not contain an issue key')
        return None
    return msg


@run_order(1)
def test_subject_does_not_contain_issue_key(msg):
    subject = msg.split('\n')[0].strip()
    first_word = subject.split()[0]
    if first_word.endswith('s') and not first_word.endswith('ss'):
        warn('Subject should use imperative mood')
    return msg


@run_order(2)
def test_body_width_and_wrap_to_limit(msg):
    lines = map(string.strip, msg.split('\n'))
    # Remove ignored lines from message
    lines = filter(lambda x: not x.startswith('#'), lines)

    too_long = map(lambda x: len(x) > MAX_BODY_WIDTH, lines)
    if any(too_long):
        info(('Some lines are longer than %i characters and will be wrapped '
              'automatically') % MAX_BODY_WIDTH)

    for i, line in enumerate(lines):
        lines[i] = textwrap.fill(line, width=MAX_BODY_WIDTH)

    return '\n'.join(lines)


if __name__ == '__main__':
    # Don't check merge message
    merge_file = os.path.join(os.path.dirname(sys.argv[1]), 'MERGE_MSG')
    if os.path.exists(merge_file):
        sys.exit(0)

    commit_msg = open(sys.argv[1]).read()
    if not commit_msg or commit_msg.startswith('\n'):
        # Git will auto abort if message is empty
        sys.exit(0)
    failure = False

    test_names = [func for func in locals().keys() if func.startswith('test')]
    tests = []
    for test_name in test_names:
        tests.append(globals()[test_name])
    tests = sorted(tests, key=lambda x: x._order)

    for test in tests:
        new_msg = test(commit_msg)
        if new_msg is None:
            failure = True
        else:
            # commit-msg hook is allowed to reformat messages
            commit_msg = new_msg

    with open(sys.argv[1], 'w') as f:
        f.write(commit_msg)

    sys.exit(int(failure))
