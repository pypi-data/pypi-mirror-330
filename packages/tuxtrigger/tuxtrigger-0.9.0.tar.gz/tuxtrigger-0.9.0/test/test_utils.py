#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT


import logging
from pathlib import Path
from test.test_configparser import MockedStdout
from unittest import mock

import pytest

from tuxtrigger import utils
from tuxtrigger.exceptions import TuxtriggerException
from tuxtrigger.repository import Branch, Repository
from tuxtrigger.utils import get_manifest, setup_logger

BASE = (Path(__file__) / "..").resolve()
SCRIPT = BASE / ".test_files/test_script.sh"

VALUE_DICT = {
    "v5.19": {
        "sha": "2437f53721bcd154d50224acee23e7dbb8d8c622",
        "ref": "refs/tags/v5.19",
    }
}


def test_pre_tux_run_none(correct_archive_read, caplog, squad_group_good):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "v5.19", "stable_plan", "example_project", None, None, None
    )
    test_branch.input_dict = VALUE_DICT
    test_branch.update_stored_data()

    with caplog.at_level(logging.INFO):
        utils.pre_tux_run(None, test_branch, True)

    assert "No script path provided" in caplog.text


def test_pre_tux_run_not_changed(correct_archive_read, caplog, squad_group_good):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "v5.19", "stable_plan", "example_project", None, None, None
    )
    test_branch.input_dict = VALUE_DICT
    test_branch.update_stored_data()

    with caplog.at_level(logging.INFO):
        utils.pre_tux_run(SCRIPT, test_branch, False)

    assert "** Repo not changed, Script not invoked" in caplog.text


@mock.patch("tuxtrigger.utils.subprocess.run")
def test_pre_tux_run(mock_run, caplog, correct_archive_read, squad_group_good):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "v5.19", "stable_plan", "example_project", None, None, None
    )
    test_branch.input_dict = VALUE_DICT
    test_branch.update_stored_data()

    ls_remote = MockedStdout(returncode=0, stdout="Success")
    mock_run.return_value = ls_remote
    with caplog.at_level(logging.INFO):
        utils.pre_tux_run(SCRIPT, test_branch, True)
    assert "performed astonishingly wonderful" in caplog.text

    ls_remote_not_zero = MockedStdout(returncode=1, stdout="", stderr="Failure")
    mock_run.return_value = ls_remote_not_zero
    with pytest.raises(TuxtriggerException) as exc:
        utils.pre_tux_run("dummy_path", test_branch, True)
    assert "Script was not invoked properly" in str(exc)


@mock.patch("tuxtrigger.utils.git_manifest_download")
def test_get_manifest(mock_download, tux_config, tux_config_kernel):
    mock_download.return_value = b"mocked manifest value"
    assert get_manifest(tux_config_kernel) == b"mocked manifest value"
    assert get_manifest(tux_config) == b""


def test_setup_logger(tmp_path):
    setup_logger(tmp_path / "test_log.txt", "DEBUG")
    assert logging.getLogger("tuxtrigger").getEffectiveLevel() == 10
    setup_logger(tmp_path / "test_log.txt", "INFO")
    assert logging.getLogger("tuxtrigger").getEffectiveLevel() == 20
    setup_logger(tmp_path / "test_log.txt", "")
    assert logging.getLogger("tuxtrigger").getEffectiveLevel() == 20
    setup_logger(tmp_path / "test_log.txt", "WARN")
    assert logging.getLogger("tuxtrigger").getEffectiveLevel() == 30
    setup_logger(tmp_path / "test_log.txt", "ERROR")
    assert logging.getLogger("tuxtrigger").getEffectiveLevel() == 40
