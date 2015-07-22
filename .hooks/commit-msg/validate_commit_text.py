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


class TermColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


MAX_SUBJECT_LENGTH = 50
MAX_BODY_WIDTH = 72


def fail(msg):
    print(TermColors.FAIL + msg + TermColors.ENDC)


def warn(msg):
    print(TermColors.WARNING + msg + TermColors.ENDC)


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


@run_order(2)
def test_body_width_and_wrap_to_limit(msg):
    lines = map(string.strip, msg.split('\n'))
    # Remove ignored lines from message
    lines = filter(lambda x: not x.startswith('#'), lines)

    too_long = map(lambda x: len(x) > MAX_BODY_WIDTH, lines)
    if any(too_long):
        warn(('Some lines are longer than %i characters and will be wrapped '
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
