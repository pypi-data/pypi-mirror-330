#
# Copyright 2022-present Linaro Limited

# SPDX-License-Identifier: MIT


from pathlib import Path
from unittest import mock
from urllib.parse import urlparse

import pytest

from tuxtrigger import configparser
from tuxtrigger.configparser import (
    _check_default_values,
    _create_squad_project,
    create_dynamic_configuration,
    present_created_config,
    update_squad_config,
)
from tuxtrigger.constants import SQUAD_CONFIG
from tuxtrigger.exceptions import TuxtriggerException
from tuxtrigger.inputvalidation import SquadConfigValidator

BASE = (Path(__file__) / "..").resolve()

HAPPY_PATH = BASE / "./test_files/happy_path.yaml"
DYNAMIC_CONFIG = {
    "squad_config": {
        "data_retention": 2137,
        "force_finishing_builds_on_timeout": True,
        "important_metadata_keys": "kernel_version,git_ref",
        "plugins": "linux_log_parser",
    },
    "repositories": [
        {
            "url": "https://git.kernel.org/pub/scm/linux/kernel/git/tomba/linux.git",
            "squad_group": "~non.existing",
            "default_plan": "test_plan.yaml",
            "default_squad_project": "example_project2",
            "default_lab": "default",
            "default_lava_test_plans_project": "https://lkft.validation.linaro.org",
            "branches": [
                {
                    "name": "master",
                    "squad_project": "example_project",
                    "plan": "stable.yaml",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
                {
                    "name": "for-laurent",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
            ],
        },
        {
            "url": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
            "squad_group": "~non.existing",
            "regex": "for-next/*",
            "default_plan": "default_plan",
            "squad_project_prefix": "testing",
            "lab": "https://lkft.validation.linaro.org",
            "lava_test_plans_project": "lkft",
            "branches": [
                {
                    "name": "master",
                    "squad_project": "example_project",
                    "plan": "stable.yaml",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
                {
                    "name": "v5.19",
                    "squad_project": "example_project",
                    "plan": "stable-next.yaml",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
                {
                    "name": "heads/test-next",
                    "squad_project": "testing-linux-heads-test-next",
                    "plan": "default_plan",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
            ],
        },
    ],
}


class MockedStdout:
    def __init__(self, returncode, stdout, stderr=None) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_create_squad_project():
    url = urlparse("https://linaro.org/repository/main.git/")
    branch = "test_branch"
    prefix = "test_prefix"

    assert _create_squad_project(url, branch, prefix) == "test_prefix-main-test_branch"
    assert _create_squad_project(url, branch, None) == "main-test_branch"


def test_check_default_values():
    assert _check_default_values(DYNAMIC_CONFIG["repositories"]) == [
        {
            "url": "https://git.kernel.org/pub/scm/linux/kernel/git/tomba/linux.git",
            "squad_group": "~non.existing",
            "default_plan": "test_plan.yaml",
            "default_squad_project": "example_project2",
            "default_lab": "default",
            "default_lava_test_plans_project": "https://lkft.validation.linaro.org",
            "branches": [
                {
                    "name": "master",
                    "squad_project": "example_project",
                    "plan": "stable.yaml",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
                {
                    "name": "for-laurent",
                    "squad_project": "example_project2",
                    "plan": "test_plan.yaml",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
            ],
        },
        {
            "url": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
            "squad_group": "~non.existing",
            "regex": "for-next/*",
            "default_plan": "default_plan",
            "squad_project_prefix": "testing",
            "lab": "https://lkft.validation.linaro.org",
            "lava_test_plans_project": "lkft",
            "branches": [
                {
                    "name": "master",
                    "squad_project": "example_project",
                    "plan": "stable.yaml",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
                {
                    "name": "v5.19",
                    "squad_project": "example_project",
                    "plan": "stable-next.yaml",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
                {
                    "name": "heads/test-next",
                    "squad_project": "testing-linux-heads-test-next",
                    "plan": "default_plan",
                    "lab": "default",
                    "lava_test_plans_project": "https://lkft.validation.linaro.org",
                },
            ],
        },
    ]


@mock.patch("tuxtrigger.configparser.subprocess.run")
def test_run_lsremote_regex(mock_run):
    mocked_run = MockedStdout(
        returncode=0,
        stdout="0066f1b0e27556381402db3ff31f85d2a2265858\trefs/heads/test-next",
    )
    mock_run.return_value = mocked_run
    assert configparser._run_lsremote_regex("example_repository", "example_regex*") == {
        "test-next": "0066f1b0e27556381402db3ff31f85d2a2265858"
    }

    mocked_run = MockedStdout(
        returncode=0,
        stdout="0066f1b0e27556381402db3ff31f85d2a2265858\trefs/heads/for/test-next",
    )
    mock_run.return_value = mocked_run
    assert configparser._run_lsremote_regex("example_repository", "example_regex*") == {
        "for/test-next": "0066f1b0e27556381402db3ff31f85d2a2265858"
    }
    failed_run = MockedStdout(returncode=1, stdout="", stderr="ls remote failure")
    mock_run.return_value = failed_run
    assert (
        configparser._run_lsremote_regex("example_repository", "example_regex*") == {}
    )


def test_create_dynamic_configuration_none():
    with pytest.raises(TuxtriggerException) as exc:
        create_dynamic_configuration(None)
    assert "Not able to generate data - config file not read" in str(exc)


@mock.patch("tuxtrigger.configparser._run_lsremote_regex")
def test_create_dynamic_configuration(mock_run):
    mock_run.return_value = {
        "heads/test-next": "0066f1b0e27556381402db3ff31f85d2a2265858"
    }
    assert configparser.create_dynamic_configuration(HAPPY_PATH) == {
        "squad_config": {
            "plugins": "linux_log_parser",
            "force_finishing_builds_on_timeout": True,
            "important_metadata_keys": "kernel_version,git_ref",
            "data_retention": 2137,
        },
        "repositories": [
            {
                "url": "https://git.kernel.org/pub/scm/linux/kernel/git/tomba/linux.git",
                "squad_group": "~non.existing",
                "branches": [
                    {
                        "name": "master",
                        "squad_project": "example_project",
                        "plan": "stable.yaml",
                        "lab": "default",
                        "lava_test_plans_project": "https://lkft.validation.linaro.org",
                    },
                    {
                        "name": "for-laurent",
                        "squad_project": "example_project",
                        "plan": "stable-next.yaml",
                        "lab": "default",
                        "lava_test_plans_project": "https://lkft.validation.linaro.org",
                    },
                ],
            },
            {
                "url": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
                "squad_group": "~non.existing",
                "regex": "for-next/*",
                "default_plan": "default_plan",
                "squad_project_prefix": "testing",
                "default_lab": "default",
                "default_lava_test_plans_project": "https://lkft.validation.linaro.org",
                "branches": [
                    {
                        "name": "master",
                        "squad_project": "example_project",
                        "plan": "stable.yaml",
                        "lab": "default",
                        "lava_test_plans_project": "https://lkft.validation.linaro.org",
                    },
                    {
                        "name": "v5.19",
                        "squad_project": "example_project",
                        "plan": "stable-next.yaml",
                        "lab": "default",
                        "lava_test_plans_project": "https://lkft.validation.linaro.org",
                    },
                    {
                        "name": "heads/test-next",
                        "squad_project": "testing-linux-heads-test-next",
                        "plan": "default_plan",
                        "lab": None,
                        "lava_test_plans_project": None,
                    },
                ],
            },
        ],
    }
    assert (
        present_created_config(configparser.create_dynamic_configuration(HAPPY_PATH))
        == 0
    )


def test_update_squad_config():
    assert update_squad_config(None) == SQUAD_CONFIG
    assert update_squad_config(
        SquadConfigValidator(**DYNAMIC_CONFIG["squad_config"])
    ) == {
        "data_retention": "2137",
        "force_finishing_builds_on_timeout": "True",
        "important_metadata_keys": "kernel_version,git_ref",
        "notification_timeout": "28800",
        "plugins": "linux_log_parser",
        "thresholds": ["build/*-warnings"],
        "wait_before_notification_timeout": "600",
        "is_public": "False",
    }
