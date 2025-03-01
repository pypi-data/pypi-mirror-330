# SPDX-FileCopyrightText: 2022 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import tomli_w

import fedrq.cli
import fedrq.cli.base

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib


@pytest.fixture
def no_tomli_w(monkeypatch, mocker):
    monkeypatch.setattr(fedrq.cli.base, "HAS_TOMLI_W", False)
    mock = mocker.patch("fedrq.cli.base.tomli_w")
    mock.dump.side_effect = NameError


def test_checkconfig_basic(run_command2):
    out = run_command2(["check-config"])
    assert "No validation errors found!" in out[0]
    assert not out[1]


def test_checkconfig_dump(run_command2, patch_config_dirs):
    defs = {"base": ["testrepo1"]}
    expected = {
        "append_system_repos": False,
        "matcher": "^(tester)$",
        "repo_aliases": {},
        "defpaths": ["testrepo1.repo"],
        "system_repos": False,
        "defs": defs,
        "repo_dirs": list(
            map(
                str,
                (
                    patch_config_dirs / "repos",
                    patch_config_dirs.parent / "global" / "repos",
                ),
            )
        ),
    }

    out = run_command2(["check-config", "--dump"])
    data = tomllib.loads(out[2])

    testrepo1 = data["releases"]["testrepo1"]
    del testrepo1["full_def_paths"]
    assert testrepo1 == expected
    assert not out[1]


def test_checkconfig_dump_error(capsys, no_tomli_w):
    with pytest.raises(SystemExit, match="tomli-w is required for --dump"):
        fedrq.cli.main(["check-config", "--dump"])
    stdout = capsys.readouterr()[0]
    assert not stdout


def test_checkconfig_default_branch_error(capsys, patch_config_dirs):
    dest: Path = patch_config_dirs / "99-default_branch_error.toml"
    data = {"default_branch": "does-not-exist"}
    with dest.open("wb") as fp:
        tomli_w.dump(data, fp)
    with pytest.raises(SystemExit, match="default_branch 'does-not-exist' is invalid"):
        fedrq.cli.main(["check-config"])
    stdout = capsys.readouterr()[0]
    assert stdout == "Validating config...\n"
