# SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import abc
import dataclasses
import importlib.resources
import logging
from collections.abc import Callable, Collection, Iterable, Iterator
from datetime import date
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Optional,
    Protocol,
    cast,
    runtime_checkable,
)
from warnings import warn

from typing_extensions import TypeVar

if TYPE_CHECKING:
    from _typeshed import StrPath
    from typing_extensions import Self, TypeAlias

    from fedrq.config import Release

# Use this trick because because the "default" kwarg (PEP 696) requires a newer
# version of typing_extensions
if TYPE_CHECKING:
    _PackageT = TypeVar(
        "_PackageT",
        bound="PackageCompat",
        default="PackageCompat",
    )
    _PackageT_co = TypeVar(
        "_PackageT_co",
        bound="PackageCompat",
        covariant=True,
        default="PackageCompat",
    )
    _PackageQueryT = TypeVar(
        "_PackageQueryT",
        bound="PackageQueryCompat",
        default="PackageQueryCompat[PackageCompat]",
    )
    _PackageQueryT_co = TypeVar(
        "_PackageQueryT_co",
        bound="PackageQueryCompat",
        covariant=True,
        default="PackageQueryCompat[PackageCompat]",
    )
    _RepoqueryT = TypeVar(
        "_RepoqueryT",
        bound="RepoqueryBase",
        default="RepoqueryBase[PackageCompat, PackageQueryCompat[PackageCompat]]",
    )
else:
    _PackageT = TypeVar("_PackageT", bound="PackageCompat")
    _PackageT_co = TypeVar("_PackageT_co", bound="PackageCompat", covariant=True)
    _PackageQueryT = TypeVar("_PackageQueryT", bound="PackageQueryCompat")
    _PackageQueryT_co = TypeVar(
        "_PackageQueryT_co", bound="PackageQueryCompat", covariant=True
    )
    _RepoqueryT = TypeVar("_RepoqueryT", bound="RepoqueryBase")
LOG = logging.getLogger("fedrq.backends")


@runtime_checkable
class PackageCompat(Protocol):  # pragma: no cover
    """
    Common interface provided by dnf.package.Package and other backends
    """

    @property
    def name(self) -> str: ...

    @property
    def arch(self) -> str: ...

    @property
    def a(self) -> str: ...

    @property
    def epoch(self) -> int: ...

    @property
    def e(self) -> int: ...

    @property
    def version(self) -> str: ...

    @property
    def v(self) -> str: ...

    @property
    def release(self) -> str: ...

    @property
    def r(self) -> str: ...

    @property
    def from_repo(self) -> str: ...

    @property
    def evr(self) -> str: ...

    @property
    def debug_name(self) -> str: ...

    @property
    def source_name(self) -> Optional[str]: ...

    @property
    def source_debug_name(self) -> str: ...

    @property
    def installtime(self) -> int: ...

    @property
    def buildtime(self) -> int: ...

    @property
    def size(self) -> int: ...

    @property
    def downloadsize(self) -> int: ...

    @property
    def installsize(self) -> int: ...

    @property
    def provides(self) -> Iterable[Any]: ...

    @property
    def requires(self) -> Iterable[Any]: ...

    @property
    def recommends(self) -> Iterable[Any]: ...

    @property
    def suggests(self) -> Iterable[Any]: ...

    @property
    def supplements(self) -> Iterable[Any]: ...

    @property
    def enhances(self) -> Iterable[Any]: ...

    @property
    def obsoletes(self) -> Iterable[Any]: ...

    @property
    def conflicts(self) -> Iterable[Any]: ...

    @property
    def sourcerpm(self) -> Optional[str]: ...

    @property
    def description(self) -> str: ...

    @property
    def summary(self) -> str: ...

    @property
    def license(self) -> str: ...

    @property
    def url(self) -> str: ...

    @property
    def reason(self) -> Optional[str]: ...

    @property
    def files(self) -> Iterable[str]: ...

    @property
    def reponame(self) -> str: ...

    @property
    def repoid(self) -> str: ...

    @property
    def vendor(self) -> str: ...

    @property
    def packager(self) -> str: ...

    @property
    def location(self) -> str: ...

    @property
    def repo(self) -> Any:
        """
        Return the package's Repo object.
        The exact object depends on which backend is used.
        """

    def remote_location(
        self, schemes: Collection[str] | None = ("http", "ftp", "file", "https")
    ) -> str | None: ...

    def __hash__(self) -> int: ...

    def __lt__(self, other) -> bool: ...

    def __le__(self, other) -> bool: ...

    def __gt__(self, other) -> bool: ...

    def __ge__(self, other) -> bool: ...


class PackageQueryCompat(
    Iterable[_PackageT_co], Generic[_PackageT_co], metaclass=abc.ABCMeta
):  # pragma: no cover
    """
    Common PackageQuery interface provided by hawkey.Query and other backends.
    When annotating function parameters and return values,
    use [`PackageQueryAlias`][fedrq.backends.base.PackageQueryAlias] instead of
    directly annotating with this type.
    """

    @abc.abstractmethod
    def filter(self, **kwargs) -> Self:
        """
        Filter the PackageQuery.
        Depending on the backend, this either modifies 'self' in place and
        return 'self' or return a new PackageQuery object.
        See https://dnf.readthedocs.io/en/latest/api_queries.html#dnf.query.Query.filter
        for the allowed kwargs.
        """
        ...

    @abc.abstractmethod
    def filterm(self, **kwargs) -> Self:
        """
        Filter the PackageQuery in place and return 'self'.
        See https://dnf.readthedocs.io/en/latest/api_queries.html#dnf.query.Query.filter
        for the allowed kwargs.
        """
        ...

    @abc.abstractmethod
    def union(self, other: Any) -> Self:
        """
        Combine two PackageQuery objects.
        Depending on the backend, this either modifies 'self' in place and
        returns 'self' or returns a new PackageQuery object.
        """
        ...

    @abc.abstractmethod
    def difference(self, other) -> Self:
        """
        Return the difference between `self` and `other`
        (packages that are in `self` but not `other`).
        Depending on the backend, this either modifies 'self' in place and
        returns 'self' or returns a new PackageQuery object.
        """

    @abc.abstractmethod
    def intersection(self, other) -> Self:
        """
        Return the difference between `self` and `other`
        (packages that are in both `self` and `other`).
        Depending on the backend, this either modifies 'self' in place and
        returns 'self' or returns a new PackageQuery object.
        """

    @abc.abstractmethod
    def __len__(self) -> int: ...

    @abc.abstractmethod
    def __iter__(self) -> Iterator[_PackageT_co]: ...


class BaseMakerBase(metaclass=abc.ABCMeta):
    """
    Create a Base object, set configuration, and load repos
    """

    base: Any

    def __init__(self, base=None) -> None:
        self.base = base

    @property
    @abc.abstractmethod
    def conf(self) -> Any:
        """
        Return the backend's Config object
        """
        ...

    @abc.abstractmethod
    def fill_sack(
        self,
        *,
        from_cache: bool = False,
        load_system_repo: bool = False,
    ) -> Any:
        """
        Fill the sack and returns the Base object.
        The repository configuration shouldn't be manipulated after this.
        'from_cache' isn't currently supported by the libdnf5 backend.
        """
        ...

    @abc.abstractmethod
    def read_system_repos(self, disable: bool = True) -> None:
        """
        Load system repositories into the base object.
        By default, they are all disabled even if 'enabled=1' is in the
        repository configuration.
        """

    @abc.abstractmethod
    def enable_repos(self, repos: Collection[str]) -> None:
        """
        Enable a list of repositories by their repoid.
        Raise a ValueError if the repoid is not in `self.base`'s configuration.
        """

    @abc.abstractmethod
    def enable_repo(self, repo: str) -> None:
        """
        Enable a repo by its id.
        Raise a ValueError if the repoid is not in `self.base`'s configuration.
        """

    @abc.abstractmethod
    def disable_repo(self, repo: str, ignore_missing: bool = True) -> None:
        """
        Disable a repo by its id.
        Raise a ValueError if the repoid is not in `self.base`'s configuration
        when ignore_missing is False.
        """

    @abc.abstractmethod
    def read_repofile(self, file: StrPath) -> None:
        """
        Load repositories from a repo file
        """

    @abc.abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration options. Must be called before reading repos.
        """
        ...

    @abc.abstractmethod
    def set_var(self, key: str, value: Any) -> None:
        """
        Set substitutions (e.g. arch, basearch, releasever).
        Needs to be called before reading repos.
        """
        ...

    # Private for now
    @abc.abstractmethod
    def _read_repofile_new(self, file: StrPath, ensure_enabled: bool = False) -> None:
        """
        Load repositories from a repo file if they're not already in the
        configuration.
        """

    def sets(self, conf: dict[str, Any], substitutions: dict[str, Any]) -> None:
        """
        Set options on the base object

        Args:
            conf:
                A dict of configuration options. Call self.set() for each k-v
                pair.
            substitutions:
                A dict of substitutions/vars options. Call self.set_var() for
                each k-v pair.
        """
        for opt in conf.items():
            self.set(*opt)
        for opt in substitutions.items():
            self.set_var(*opt)

    def load_filelists(self, enable: bool = True) -> None:  # noqa: ARG002
        # Can be overriden by subclasses. Purposely isn't an @abstractmethod.
        """
        Load the filelists if they're not already enabled by default

        Args:
            enable:
                Whether to enable or disable filelists
        """
        return None

    @abc.abstractmethod
    def load_changelogs(self, enable: bool = True) -> None:
        """
        Load changelog metadata

        Args:
            enable:
                Whether to enable or disable filelists
        """

    def load_release_repos(self, release: Release, set_releasever: bool = True) -> None:
        """
        Load the repositories from a fedrq.config.Release object

        Args:
            release:
                [`Release`][fedrq.config.Release] object
            set_releasever:
                Whether to set the `$releasever` based on the release or just
                leave it alone
        """
        if set_releasever:
            self.set_var("releasever", release.version)
        if release.release_config.system_repos:
            self.read_system_repos(
                disable=not release.release_config.append_system_repos
            )
        for path in release.release_config.full_def_paths:
            with importlib.resources.as_file(path) as fp:
                LOG.debug("Reading %s", fp)
                self._read_repofile_new(fp)
        release.repog.load(self, release.config, release)

    @abc.abstractmethod
    def create_repo(self, repoid: str, **kwargs: Any) -> None:
        """
        Add a Repo object to the repo sack and configure it.

        Args:
            repoid:
                Repository ID
            kwargs:
                key-values options that should be set on the Repo object values
                (like $basearch) will be substituted automatically.
        """
        ...

    @property
    @abc.abstractmethod
    def backend(self) -> BackendMod: ...

    @abc.abstractmethod
    def repolist(self, enabled: bool | None = None) -> list[str]: ...

    @abc.abstractmethod
    def enable_source_repos(self) -> None:
        """
        Enable the corresponding -source repos of the currently enabled
        repositories
        """
        ...


class NEVRAFormsCompat(Protocol):
    NEVRA: int
    NEVR: int
    NEV: int
    NA: int
    NAME: int


class RepoqueryBase(Generic[_PackageT_co, _PackageQueryT_co], metaclass=abc.ABCMeta):
    """
    Helpers to query a repository.
    Provides a unified repoquery interface for different backends.
    When annotating function parameters and return values,
    use [`RepoqueryAlias`][fedrq.backends.base.RepoqueryAlias] instead of
    directly annotating with this type.
    """

    def __init__(self, base) -> None:
        self.base = base

    @property
    @abc.abstractmethod
    def base_arches(self) -> set[str]:
        """
        Return a set of the system's arch and basearch.
        """
        ...

    def _get_resolve_options(
        self,
        resolve: bool,
        with_filenames: bool | None,
        with_provides: bool | None,
        resolve_provides: bool | None,
    ) -> dict[str, Any]:
        opts: dict[str, bool | None] = {
            "with_filenames": with_filenames,
            "with_provides": with_provides,
            "resolve_provides": resolve_provides,
        }
        return {key: resolve if opt is None else opt for key, opt in opts.items()}

    @abc.abstractmethod
    def resolve_pkg_specs(
        self,
        specs: Collection[str],
        resolve: bool = False,
        latest: int | None = None,
        with_src: bool = True,
        *,
        with_filenames: bool | None = None,
        with_provides: bool | None = None,
        resolve_provides: bool | None = None,
        nevra_forms: list[int] | None = None,
    ) -> _PackageQueryT_co:
        """
        Resolve pkg specs.
        See
        https://dnf.readthedocs.io/en/latest/command_ref.html?highlight=spec#specifying-packages
        or
        https://dnf5.readthedocs.io/en/latest/misc/specs.7.html
        for valid forms.

        Args:
            specs:
                Package specs to resolve.
            resolve:
                Whether to resolve file paths or virtual Provides in addition
                to package specs
            latest:
                Limit packages with the same name and arch.
            with_src:
                Whether to consider `.src` packages when resolving `specs`
        """
        ...

    def arch_filterm(
        self,
        query: _PackageQueryT,
        arch: str | Iterable[str] | None = None,
    ) -> _PackageQueryT:
        """
        Filter a query's architectures in place and return it.
        It includes a little more functionality than query.filterm(arch=...).

        - When arch is None, the query is left untouched.
        - If arch equals 'notsrc', all src and multilib packages are
          excluded.
        - If arch equals 'arched', all noarch, multilib, and source
          packages are excluded.
        - Otherwise, arch is passed to query.filterm(arch=...) and no other
          validation is preformed.
        """
        if not arch:
            return query
        if arch == "notsrc":
            return query.filterm(arch=(*self.base_arches, "noarch"))  # type: ignore
        elif arch == "arched":
            return query.filterm(arch=self.base.conf.basearch)
        else:
            return query.filterm(arch=arch)

    def arch_filter(
        self,
        query: _PackageQueryT,
        arch: str | Iterable[str] | None = None,
    ) -> _PackageQueryT:
        """
        Filter a query's architectures and return it.
        It includes a little more functionality than query.filter(arch=...).

        - When arch is None, the query is left untouched.
        - If arch equals 'notsrc', all src and multilib packages are
          excluded.
        - If arch equals 'arched', all noarch, multilib, and source
          packages are excluded.
        - Otherwise, arch is passed to query.filterm(arch=...) and no other
          validation is preformed.
        """
        if not arch:
            return query
        if arch == "notsrc":
            return query.filter(arch=(*self.base_arches, "noarch"))  # type: ignore
        if arch == "arched":
            return query.filter(arch=list(self.base_arches))
        return query.filter(arch=arch)

    @abc.abstractmethod
    def _query(self) -> _PackageQueryT_co:
        """
        Return the PackageQuery object for this backend
        """
        return self.base.sack.query()

    def query(
        self,
        *,
        arch: str | Iterable[str] | None = None,
        **kwargs,
    ) -> _PackageQueryT_co:
        """
        Return an inital PackageQuery that's filtered with **kwargs.
        Further filtering can be applied with the PackageQuery's filter and
        filterm methods.
        """
        if kwargs.get("latest") is None:
            kwargs.pop("latest", None)
        query = self._query()
        query.filterm(**kwargs)
        self.arch_filterm(query, arch)
        return query

    def get_package(
        self,
        name: str,
        arch: str | Iterable[str] | None = None,
    ) -> _PackageT_co:
        """
        Return the latest Package that matches the 'name' and 'arch'.
        A ValueError is raised when no matches are found.
        """
        query = self.query(name=name, arch=arch, latest=1)
        if len(query) < 1:
            raise ValueError(f"Zero packages found for {name} on {arch}")
        return cast("_PackageT_co", next(iter(query)))

    def get_subpackages(
        self, packages: Iterable[PackageCompat], **kwargs
    ) -> _PackageQueryT_co:
        """
        Return a PackageQuery containing the binary RPMS/subpackages produced
        by {packages}.

        Args:
            packages:
                An interable of `PackageCompat` containing source packages
        """
        arch = kwargs.get("arch")
        if arch == "src":
            raise ValueError("{arch} cannot be 'src'")
        elif not arch:
            kwargs.setdefault("arch__neq", "src")
        if val := kwargs.pop("sourcerpm", None):
            warn(f"Removing invalid kwarg: 'sourcerpm={val}")

        for package in packages:
            if package.arch != "src":
                raise ValueError(f"{package} must be a source package.")

        sourcerpms = [
            f"{package.name}-{package.version}-{package.release}.src.rpm"
            for package in packages
        ]
        query = self.query(sourcerpm=sourcerpms, **kwargs)
        return query

    @property
    @abc.abstractmethod
    def backend(self) -> BackendMod: ...


RepoqueryAlias: TypeAlias = RepoqueryBase


@dataclasses.dataclass(frozen=True)
class ChangelogEntry:
    """
    Data class for changelog entry data.
    Do not instantiate directly!
    """

    text: str
    author: str
    date: date

    def __str__(self) -> str:
        date_str = format(self.date, "%a %b %d %Y")
        return f"* {date_str} {self.author}\n{self.text}"


class _get_changelogs(Protocol):
    def __call__(self, package: Any) -> Iterator[ChangelogEntry]:
        """
        Args:
            package:
                A backend's Package object
        """
        ...


class BackendMod(Protocol):
    """
    Protocol for a fedrq backend module.
    Each backend module (e.g.
    [`fedrq.backends.dnf.backend`][fedrq.backends.dnf.backend])
    implements this interface.
    """

    BACKEND: str
    BaseMaker: type[BaseMakerBase]
    Package: type[PackageCompat]
    NEVRAForms: type[NEVRAFormsCompat]
    PackageQuery: type[PackageQueryCompat]
    PackageQueryAlias: type[PackageQueryCompat]
    Repoquery: type[RepoqueryBase]
    RepoError: type[BaseException]
    get_releasever: Callable[[], str]
    get_changelogs: _get_changelogs


PackageQueryAlias: TypeAlias = PackageQueryCompat
