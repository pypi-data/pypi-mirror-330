# SPDX-FileCopyrightText: 2022 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from shutil import rmtree

import pytest

import fedrq.cli
from fedrq import config as rqconfig
from fedrq.backends import get_default_backend
from fedrq.backends.base import BackendMod

TEST_DATA = Path(__file__).parent.resolve() / "test_data"

TEST_REPO_1 = f"""
[testrepo1]
name = testrepo1
baseurl = file://{TEST_DATA / 'repos' / 'repo1' / 'repo'}/
gpgcheck = False
"""

TEST_CONFIG_1 = """
default_branch = "tester"

[releases.testrepo1]
matcher = "^(tester)$"
defs.base = ["testrepo1"]
defpaths = ["testrepo1.repo"]
system_repos = false
"""

# @pytest.fixture(scope="session", autouse=True)


@pytest.fixture(scope="session", autouse=True)
def clear_cache():
    path = rqconfig.get_smartcache_basedir() / "tester"
    rmtree(path, ignore_errors=True)
    try:
        yield
    finally:
        rmtree(path, ignore_errors=True)


@pytest.fixture(scope="session", autouse=True)
def default_backend():
    backend = os.environ.get("FEDRQ_BACKEND")
    gotten = get_default_backend(backend, bool(backend))
    # Check that get_default_backend does the right thing
    assert (backend or gotten.BACKEND) == gotten.BACKEND
    return gotten


@pytest.fixture
def temp_smartcache(monkeypatch, tmp_path):
    path = tmp_path / "smartcache"
    path.mkdir()
    monkeypatch.setenv("XDG_CACHE_HOME", str(path))
    return path


@pytest.fixture
def data_path():
    return TEST_DATA


@pytest.fixture(scope="session", autouse=True)
def repo_test_repo():
    assert TEST_DATA.is_dir()
    assert (buildsh := TEST_DATA / "build.sh").exists()
    subprocess.run(("bash", buildsh), check=True)


@pytest.fixture(autouse=True)
def clear_config(monkeypatch):
    monkeypatch.setattr(rqconfig, "CONFIG_DIRS", ())


@pytest.fixture
def patch_config_dirs(tmp_path, monkeypatch):
    config_dirs = (tmp_path / "custom", tmp_path / "global")
    for d in config_dirs:
        d.mkdir()

    conf = config_dirs[1]
    conf.joinpath("test.toml").write_text(TEST_CONFIG_1)

    repo_dir = conf.joinpath("repos")
    repo_dir.mkdir()
    repo_dir.joinpath("testrepo1.repo").write_text(TEST_REPO_1)

    monkeypatch.setattr(rqconfig, "CONFIG_DIRS", config_dirs)
    return config_dirs[0]


@pytest.fixture
def repo_test_config(patch_config_dirs) -> rqconfig.RQConfig:
    return rqconfig.get_config(load_filelists="always", load_other_metadata=True)


@pytest.fixture
def repo_test_rq(repo_test_config: rqconfig.RQConfig, default_backend: BackendMod):
    return repo_test_config.get_rq("tester", "base")


@pytest.fixture(scope="session")
def target_cpu():
    macro = subprocess.run(
        ["rpm", "-E", "%_target_cpu"], text=True, capture_output=True, check=True
    ).stdout.strip()
    assert macro != "%{_target_cpu}"
    return macro


@pytest.fixture
def runs(capsys):
    def runner(args, return_stdout=True):
        fedrq.cli.main(args)
        stdout, stderr = capsys.readouterr()
        result = [stdout.splitlines(), stderr.splitlines()]
        if return_stdout:
            result.append(stdout)
        return result

    return runner


@pytest.fixture
def run_command2(runs, patch_config_dirs):
    return runs
