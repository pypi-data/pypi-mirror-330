<!--
SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
SPDX-License-Identifier: GPL-2.0-or-later
-->

# fedrq's Python API

The `fedrq.config` module and the `fedrq.backends` package are public API.
Everything under `fedrq.cli` is internal.
fedrq is primarily a CLI tool and its API only abstracts the specific
dnf/libdnf5 functionality that the CLI uses.
The API's main purpose is "repoquerying",
but you can use the fedrq functionality you'd like and then access the
underlying dnf Base object to preform other tasks if needed.

Take a look at the docstrings — in particular the base classes' documentation — 
for more information.

!!! warning

    The `fedrq.backends.**.experimental` modules are not meant for
    public use.
    They are subject to breaking changes in minor releases and should not be
    relied on by external code.
    Once the functionality has stabilized, the code will be moved out of the
    experimental namespace.

## fedrq.backends

`fedrq.backends` is the heart of fedrq's API.
There is a dnf backend (`fedrq.backends.dnf`)
and a libdnf5 backend (`fedrq.backends.libdnf5`).
This package provides an interface to configure a Base session, load
repositories, preform queries, and related functionality.
The main primitives are:

### BaseMaker

**Base class**: [`fedrq.backends.base.BaseMakerBase`][fedrq.backends.base.BaseMakerBase]

**dnf backend:** [`fedrq.backends.dnf.backend.BaseMaker`][fedrq.backends.dnf.backend.BaseMaker]

**libdnf5 backend:** [`fedrq.backends.libdnf5.backend.BaseMaker`][fedrq.backends.libdnf5.backend.BaseMaker]

`BaseMaker` allows configuring a dnf `Base` session and loading repositories.

### Repoquery

**Base class**: [`fedrq.backends.base.RepoqueryBase`][fedrq.backends.base.RepoqueryBase]

**dnf backend:** [`fedrq.backends.dnf.backend.Repoquery`][fedrq.backends.dnf.backend.Repoquery]

**libdnf5 backend:** [`fedrq.backends.libdnf5.backend.Repoquery`][fedrq.backends.libdnf5.backend.Repoquery]

`Repoquery` accepts an initialized Base object (see `BaseMaker`) and allows
performing a large range of queries. Most of its methods return
`PackageQueryCompat` or `PackageCompat` objects.


### PackageQueryCompat

**Protocol:** [`fedrq.backends.base.PackageQueryCompat`][fedrq.backends.base.PackageQueryCompat]

**dnf backend:** [`fedrq.backends.dnf.backend.PackageQuery`][fedrq.backends.dnf.backend.PackageQuery] -> [`hawkey.Query`][dnf.query.Query]

**libdnf5 backend:** [`fedrq.backends.libdnf5.backend.PackageQuery`][fedrq.backends.libdnf5.backend.PackageQuery]
([`libdnf5.rpm.PackageQuery`][libdnf5.rpm.PackageQuery] subclass)

`PackageQueryCompat` is a set-like object of `PackageCompat` objects. It contains
methods to filter its Packages based on certain criteria. Typically, you would
access the filtering methods through the `Repoquery` class's wrappers.

- `fedrq.backends.libdnf5.backend.PackageQuery` --- subclass of
  `libdnf5.rpm.PackageQuery`. adds back missing `query` and `querym` methods.


### PackageCompat


**Protocol:** [`fedrq.backends.base.PackageCompat`][fedrq.backends.base.PackageCompat]

**dnf backend:** [`fedrq.backends.dnf.backend.Package`][fedrq.backends.dnf.backend.Package] -> [`dnf.package.Package`][dnf.package.Package]

**libdnf5 backend:** [`fedrq.backends.libdnf5.backend.Package`][fedrq.backends.libdnf5.backend.Package]
([`libdnf5.rpm.Package`][libdnf5.rpm.Package] subclass)

- [`fedrq.backends.libdnf5.backend.Package`][fedrq.backends.libdnf5.backend.Package] ---
  subclass of [`libdnf5.rpm.Package`][libdnf5.rpm.Package]
  that implements missing functionality and compatibility with
  [`dnf.package.Package`][dnf.package.Package].
  The subclass includes properties to access Package attributes.
  These properties were removed from libdnf5 in favor of `get_foo()` methods.
  It also includes rich comparison support (`__lt__`, `__gt__`, etc.) and
  implements roughly the same sort order as the dnf backend and adds a
  `__hash__()` method so it can e.g., be used in a set or as a dictionary key.

    Importing
    [`fedrq.backends.libdnf5.backend`][fedrq.backends.libdnf5.backend]
    registers the `Package` subclass so PackageQuery contains our subclass.

## [`fedrq.config`][fedrq.config]

Most of the code here should not be called directly. Use `get_config()` to load
the configuration from the filesystem. Create an `RQConfig` object manually if
you must.

This example shows how to load the configuration and preform a basic query.

``` python
# SPDX-License-Identifier: Unlicense
# SPDX-FileCopyrightText: None

# Roughly equivalent to:
#     fedrq whatrequires --arch=noarch -b rawhide -r buildroot bash | grep '^a'

from fedrq.config import get_config, RQConfig

# The get_config() function returns an RqConfig object.
#
# Load config from filesystem and override some options
config = get_config(backend="libdnf5")

# The RQConfig.get_rq() method returns a Repoquery object.
# Repoquery is fedrq's helper class to perform various types of package queries.
#
# This creates a Repoquery containing the Fedora Rawhide koji buildroot repositories.
# get_rq() supports any release configuration builtin to fedrq
# or configured on your local system.
rq = config.get_rq("rawhide", "buildroot")

# The Repoquery.query() method returns a PackageQuery implementation.
#
# This gets all noarch packages that start with 'a' and depend on bash
query = rq.query(
    name__glob="a*", arch="noarch", requires=rq.query(name="bash", arch="notsrc")
)
# By using sorted(), you'll get (relatively) consistent ordering between backends
for package in sorted(query):
    print(package)
```


## Examples

See [api-examples] for some simple example code.

Real world examples:

- [mkblocker.py] - given a list of source packages names, use jinja2 to
  template a specfile that Conflicts on every subpackage produced by the source
  packages. This was used as part of the [Mass_Retire_Golang_Leaves] Fedora Change.
- [sig_policy.py] - enforces the FESCo [SIG Policy][sig-policy] by using fedrq
  to find packages that meet certain criteria and adding the corresponding SIG
  to the distgit repo's ACLs.

[api-examples]: https://git.sr.ht/~gotmax23/fedrq/tree/main/item/contrib/api_examples
[mkblocker.py]: https://git.sr.ht/~gotmax23/fedora-scripts/tree/main/item/go-sig/blocker/mkblocker.py
[Mass_Retire_Golang_Leaves]: https://fedoraproject.org/wiki/Changes/Mass_Retire_Golang_Leaves#Implementation
[sig_policy.py]: https://pagure.io/releng/blob/main/f/scripts/fesco/sig-policy/sig_policy.py
[sig-policy]: https://docs.fedoraproject.org/en-US/fesco/SIG_policy/
