# Gatekeeper

Gatekeeper is a small shell script that lets you easily set up and manage hooks for
your git repositories.

## Install

```
$ curl https://raw.githubusercontent.com/joshfriend/gatekeeper/master/gatekeeper.sh
$ ./gatekeeper.sh --install
Hooking you up...
```

**Note:** This process will overwrite any existing git hooks!

## How It Works

Gatekeeper installs itself with a symlink as the following git hooks (see
[the docs][githooks-docs] for details on when each of these is executed and
what arguments they take):

* `applypatch-msg`
* `commit-msg`
* `post-update`
* `pre-applypatch`
* `pre-commit`
* `pre-push`
* `pre-rebase`
* `prepare-commit-msg`
* `update`

When Git runs a hook, Gatekeeper will look in the `.githooks` directory in your
repo root for a folder with the name of the hook that Git is running. All
executable scripts in that folder will be executed in alphabetic order. If one
of the hooks returns a non-zero exit code, any remaining hooks are skipped and
Gatekeeper will indicate hook failure to Git.

## Example

Given a `.githooks` directory containing the following:

```
repo/
    .githooks/
        pre-commit/
            bar.py
            foo.sh
```

Contents of `bar.py`:

```python
#!/usr/bin/env python
print 'bar'
```

Contents of `foo.sh`:

```bash
#!/bin/bash
echo "foo"
```

Running `git commit` will have this result:

```
$ git commit
bar
foo
Aborting commit due to empty commit message.
```

More examples can be found in the [`examples/` directory][examples-dir]

## Skipping Hooks

If you would like to bypass your hooks temporarily, just pass an additional
`--no-verify` flag to any Git operation. For more info read the `githooks(5)`
manpages:

```
$ man githooks
```

The `--no-verify` flag is all-or-nothing. You cannot skip individual hooks
selectively.

[githooks-docs]: http://git-scm.com/docs/githooks
[examples-dir]: https://github.com/joshfriend/gatekeeper/tree/master/examples
