#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import gzip
from pathlib import Path
from test.test_configparser import MockedStdout
from unittest import mock

import pytest

from tuxtrigger.exceptions import SquadException, TuxtriggerException
from tuxtrigger.repository import Branch, Repository

VALUE_DICT = {
    "v5.19": {
        "sha": "2437f53721bcd154d50224acee23e7dbb8d8c622",
        "ref": "refs/tags/v5.19",
    }
}
VALUE = "v5.19"
RIGHT_KEY = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git"
WRONG_KEY = "/linux-not-existing"
FINGERPRINT = "eb054f9048d6a8c3de909d97cf7ae080662f591c"

BASE = (Path(__file__) / "..").resolve()
PLAN_PATH = BASE / "stable.yaml"


class MockedSquadGroup:
    def __init__(self, sq_group, sq_project):
        self.sq_group = sq_group
        self.sq_project = sq_project

    def project(self, *args):
        self.id = 2137
        if self.sq_project is None:
            self.id = 12
            return self.id
        return self


@mock.patch("tuxtrigger.manifest.git_repository_fingerprint")
def test_load_fingerprint(mock_manifest, squad_group_good):
    with open(BASE / "test_files/manifest.js.gz", "rb") as gzip_file:
        with gzip.open(gzip_file, "rb") as test_file:
            mock_manifest.return_value = test_file.read()
            test_repository = Repository(
                "http://not_existing_path/repository.git", squad_group_good
            )
            test_repository.load_fingerprint(mock_manifest.return_value)

            assert test_repository.fingerprint == ""

            test_repository_kernel = Repository(
                "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
                squad_group_good,
            )
            test_repository_kernel.load_fingerprint(mock_manifest.return_value)

            assert test_repository_kernel.fingerprint == FINGERPRINT


def test_check_fingerprint(
    wrong_archive_read,
    correct_archive_read,
    correct_archive_read_no_fingerprint,
    squad_group_good,
):
    test_repository = Repository(
        "http://not_existing_path/repository.git", squad_group_good
    )
    test_repository_kernel = Repository(
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
        squad_group_good,
    )
    test_repository.fingerprint = ""
    test_repository_kernel.fingerprint = "1234"
    # Archive is empty
    assert test_repository.check_fingerprint(wrong_archive_read) is False
    # No 'fingerprint' entry in archive
    assert (
        test_repository_kernel.check_fingerprint(correct_archive_read_no_fingerprint)
        is False
    )
    # Fingreprint exist in archive
    assert test_repository_kernel.check_fingerprint(correct_archive_read) is False
    # Fingerprint exists in archive and no changes
    test_repository_kernel.fingerprint = FINGERPRINT
    assert test_repository_kernel.check_fingerprint(correct_archive_read) is True

    # no key in File
    assert (
        test_repository.check_fingerprint(correct_archive_read_no_fingerprint) is False
    )


@mock.patch("tuxtrigger.repository.subprocess.run")
def test_get_sha_value(mock_run, squad_group_good):
    ls_remote = MockedStdout(
        returncode=0,
        stdout="0066f1b0e27556381402db3ff31f85d2a2265858        refs/heads/master",
    )
    mock_run.return_value = ls_remote
    test_repo = Repository(
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
        squad_group_good,
    )
    test_branch = Branch(
        test_repo, "master", "stable_plan", "example_project", None, None, None
    )
    assert test_branch.get_sha_value() == {
        "master": {
            "ref": "refs/heads/master",
            "sha": "0066f1b0e27556381402db3ff31f85d2a2265858",
        }
    }
    ls_remote_error = MockedStdout(returncode=1, stdout="", stderr="Serious Error")
    mock_run.return_value = ls_remote_error
    assert test_branch.get_sha_value() == {"master": {"sha": "", "ref": ""}}


@mock.patch("tuxtrigger.repository.Branch.get_sha_value")
def test_compare_sha(
    mock_sha, wrong_archive_read, correct_archive_read, squad_group_good
):
    mock_sha.return_value = VALUE_DICT
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "v5.19", "stable_plan", "example_project", None, None, None
    )

    assert test_branch.compare_sha() is True

    test_repo.repository_url = (
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git"
    )
    test_branch.branch = "v5.19"
    assert test_branch.__str__() == "v5.19"
    assert test_branch.compare_sha() is True
    test_branch.stored_data = {test_repo.repository_url: VALUE_DICT}
    assert test_branch.compare_sha() is False
    test_branch.stored_data = {
        test_repo.repository_url: {"v5.19": {"sha": "1234", "ref": "refs/tags/v5.19"}}
    }
    assert test_branch.compare_sha() is True
    test_branch.branch = "not_existing"
    assert test_branch.compare_sha() is True
    test_branch.stored_data = {
        test_repo.repository_url: {test_branch: {"sha": "", "ref": ""}}
    }
    assert test_branch.compare_sha() is True


def test_update_stored_data(squad_group_good):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "v5.19", "stable_plan", "example_project", None, None, None
    )
    test_branch.input_dict = VALUE_DICT

    test_branch.update_stored_data()
    assert test_branch.stored_data == VALUE_DICT


@mock.patch("tuxtrigger.repository.create_or_update_project")
@mock.patch("tuxtrigger.repository.Squad.group")
def test_squad_project(mock_group, mock_call, capsys):
    test_repo = Repository("not_existing_url", "example")
    test_branch = Branch(
        test_repo, "v5.19", "stable_plan", "example_project", None, None, None
    )
    mock_group.return_value = None
    with pytest.raises(SquadException) as exc:
        test_branch.check_squad_project()
        assert (
            f"*SQUAD response error - group {test_branch.repository.squad_group} not found"
            in str(exc)
        )

    mock_group.return_value = MockedSquadGroup("example_group", "existing_project")
    mock_call.return_value = (type("", (), {"id": "2137"})(), None)
    test_branch.check_squad_project()
    assert test_branch.squad_project_id == "2137"
    mock_group.return_value = MockedSquadGroup("example_group2", None)
    mock_call.return_value = (type("", (), {"id": "12"})(), None)
    test_branch.check_squad_project()
    assert test_branch.squad_project_id == "12"


@mock.patch("tuxtrigger.repository.SubmitTuxSuiteCommand.run")
def test_squad_submit_tuxsuite(mock_call):
    test_repo = Repository("not_existing_url", None)
    test_branch = Branch(
        test_repo, "v5.19", "stable_plan", "example_project", None, None, None
    )
    with pytest.raises(TuxtriggerException) as exc:
        test_branch.squad_submit_tuxsuite({}, PLAN_PATH)
        assert "** SQUAD config is not available! Unable to process **" in str(exc)

    test_branch.repository.squad_group = "existing_one"
    test_branch.squad_submit_tuxsuite({"git_describe": "2137"}, PLAN_PATH)
    mock_call.assert_called()


@mock.patch("tuxtrigger.repository.register_callback")
def test_register_callback(mock_call):
    test_repo = Repository("not_existing_url", None)
    test_branch = Branch(
        test_repo, "v5.19", "stable_plan", "example_project", None, None, None
    )
    with pytest.raises(TuxtriggerException) as exc:
        test_branch.register_squad_callback({}, "callback_url")
        assert "** SQUAD config is not available! Unable to process **" in str(exc)

    test_branch.repository.squad_group = "existing_one"
    mock_call.return_value = (type("", (), {"registered": True}), None)
    test_branch.register_squad_callback({"git_describe": "2137"}, "callback_url")
    mock_call.assert_called()

    mock_call.return_value = (None, "terrible exception")
    with pytest.raises(SquadException) as exc:
        test_branch.register_squad_callback({"git_describe": "2137"}, "callback_url")
        assert (
            "*SQUAD response error - not able to register callback for callback_url"
            in str(exc)
        )
