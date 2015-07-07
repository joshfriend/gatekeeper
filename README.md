# Hooker

> We'll create our own workflow with Git and Hooker!

Hooker is a small shell script that lets you easily set up and manage hooks for
your git repositories.

## Install

```
$ curl https://raw.githubusercontent.com/joshfriend/hooker/master/hooker.sh
$ ./hooker.sh --install
Hooking you up...
```

## How It Works

Hooker installs itself with a symlink as the following git hooks (see
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

When Git runs a hook, Hooker will look in the `.hooks` directory in your repo
root for a folder with the name of the hook that Git is running. All executable
scripts in that folder will be executed in alphabetic order. If one of the
hooks returns a non-zero exit code, any remaining hooks are skipped and Hooker
will indicate hook failure to Git.

## Example

Given a `.hooks` directory containing the following:

```
repo/
    .hooks/
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

[githooks-docs]: http://git-scm.com/docs/githooks
[examples-dir]: https://github.com/joshfriend/hooker/tree/master/examples