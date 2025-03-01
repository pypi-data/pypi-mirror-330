<!--
SPDX-FileCopyrightText: 2022 Maxwell G <gotmax@e.email>
SPDX-License-Identifier: GPL-2.0-or-later
-->

# Contributing

This project's mailing list is [~gotmax23/fedrq@lists.sr.ht][mailto]
([archives]).

Development, issue reporting, and project discussion happen on the mailing
list.

## Issue Reporting and Feature Requests

Direct these to the mailing list. fedrq has a [ticket tracker][tracker] on
todo.sr.ht, but it's only for confirmed issues.

[tracker]: https://todo.sr.ht/~gotmax23/fedrq

## Patches

Contributions are always welcome!
It is recommended that you send a message to the mailing list before working on
a larger change.

Patches can be sent to [~gotmax23/fedrq@lists.sr.ht][mailto]
using [`git send-email`][1].
No Sourcehut account is required!

After configuring git-send-email as explained at [git-send-email.io][1]:

[mailto]: mailto:~gotmax23/fedrq@lists.sr.ht
[archives]: https://lists.sr.ht/~gotmax23/fedrq
[1]: https://git-send-email.io

```
git clone https://git.sr.ht/~gotmax23/fedrq
cd fedrq

# First time only
git config sendemail.to "~gotmax23/fedrq@lists.sr.ht"
git config format.subjectprefix "PATCH fedrq"

python3 -m venv venv --system-site-packages
. ./venv/bin/activate
pip install -U -e . nox

$EDITOR ...

sudo dnf copr enable -y rpmsoftwaremanagement/dnf5-unstable
nox
nox -e mockbuild

git commit -a
git send-email origin/main
```

See [git-send-email.io][1] for more details.

If you prefer, git.sr.ht has a webui to help you submit patches to a mailing
list that can be used in place of `git send-email`. You can follow [this
written guide][2] or [this video guide][3] for how to use the webui.

[2]: https://man.sr.ht/git.sr.ht/#sending-patches-upstream
[3]: https://spacepub.space/w/no6jnhHeUrt2E5ST168tRL


## Linting and Unit Tests

Unit tests are run with `pytest`.
This project uses isort and black to format code, ruff for linting, and mypy
for type checking.
`reuse lint` is used to ensure that code follows the REUSE specification.
You can run all of these tools using nox. Simply install nox with pip or dnf.
The tests also require the `rpm-build` and createrepo_c` and packages.

CI also runs a mock build against rawhide.
Run `nox -e srpm` to build an SRPM containing the git HEAD
or run `nox -e mockbuild` to preform a build in mock.

builds.sr.ht runs CI for patches sent to the mailing list,
but please run the tests locally before submitting your changes.
See the [.builds] directory for the CI workflow configuration.

[.builds]: https://git.sr.ht/~gotmax23/fedrq/tree/main/item/.builds
