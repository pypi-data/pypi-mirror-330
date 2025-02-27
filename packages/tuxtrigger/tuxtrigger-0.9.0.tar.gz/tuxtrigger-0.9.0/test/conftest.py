#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

from tuxtrigger.inputvalidation import TuxtriggerConfiguration
from tuxtrigger.yamlload import yaml_file_read

BASE = (Path(__file__) / "..").resolve()

ERROR_PATH = BASE / "./test_files/error_path.yaml"
HAPPY_PATH = BASE / "./test_files/happy_path.yaml"
GITSHA_FILE = BASE / "./test_files/gitsha.yaml"
GITSHA_FILE_2 = BASE / "./test_files/gitsha2.yaml"


@pytest.fixture
def wrong_archive_read():
    try:
        return yaml_file_read(Path("non_existing_file"))
    except FileNotFoundError:
        return None


@pytest.fixture
def correct_archive_read_no_fingerprint():
    return yaml_file_read(GITSHA_FILE_2)


@pytest.fixture
def correct_archive_read():
    return yaml_file_read(GITSHA_FILE)


@pytest.fixture
def repo_setup_error():
    return TuxtriggerConfiguration.create_repo_list(yaml_file_read(ERROR_PATH))


@pytest.fixture
def repo_setup_good():
    return TuxtriggerConfiguration.create_repo_list(yaml_file_read(HAPPY_PATH))


@pytest.fixture
def squad_group_good():
    return "~non.existing"


@pytest.fixture
def tux_config():
    config = {
        "config": {
            "plugins": "linux_log_parser",
            "force_finishing_builds_on_timeout": True,
            "important_metadata_keys": "kernel_version,git_ref",
            "data_retention": 2137,
        },
        "repositories": [
            {
                "url": "http://not_existing_path/repository.git",
                "squad_group": "~pawel.szymaszek",
                "default_plan": "stable.yaml",
                "default_squad_project": "test_yaml_file",
                "branches": [
                    {
                        "name": "master",
                        "plan": "stable.yaml",
                        "squad_project": "test_yaml_file",
                    },
                ],
            }
        ],
    }

    return TuxtriggerConfiguration(
        config, BASE, BASE / "output.yaml", disable_squad=False
    )


@pytest.fixture
def tux_config_kernel():
    config = {
        "config": {
            "plugins": "linux_log_parser",
            "force_finishing_builds_on_timeout": True,
            "important_metadata_keys": "kernel_version,git_ref",
            "data_retention": 2137,
        },
        "repositories": [
            {
                "url": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
                "squad_group": "~pawel.szymaszek",
                "default_plan": "stable.yaml",
                "default_squad_project": "test_yaml_file",
                "branches": [
                    {
                        "name": "master",
                        "plan": "stable.yaml",
                        "squad_project": "test_yaml_file",
                    },
                    {
                        "name": "v6.6",
                        "plan": "stable.yaml",
                        "squad_project": "test_yaml_file",
                    },
                    {
                        "name": "v6.5",
                        "plan": "stable.yaml",
                        "squad_project": "test_yaml_file",
                    },
                ],
            }
        ],
    }

    return TuxtriggerConfiguration(config, BASE, BASE / "output.yaml")


@pytest.fixture(autouse=True)
def squad_env_setup(monkeypatch):
    monkeypatch.setenv("SQUAD_TOKEN", "some-value")


@pytest.fixture(autouse=True)
def squad_env_host(monkeypatch):
    monkeypatch.setenv("SQUAD_HOST", "https://dummy-qa-reports.org")
