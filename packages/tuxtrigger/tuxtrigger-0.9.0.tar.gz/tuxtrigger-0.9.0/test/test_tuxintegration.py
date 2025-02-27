#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import json
from pathlib import Path
from test.test_configparser import MockedStdout
from unittest import mock

import pytest

from tuxtrigger.exceptions import TuxsuiteException, TuxtriggerException
from tuxtrigger.repository import Branch, Repository
from tuxtrigger.tuxintegration import (
    TuxSuiteIntegration,
    tux_plan_submitter,
    tuxsuite_trigger,
)

BASE = (Path(__file__) / "..").resolve()

PLAN = BASE / "test_files/planTest.yaml"
PLAN_FAIL = BASE / "test_files/planTestc.yaml"
JSON_PLAN_RESULT = BASE / "test_files/plan_result.json"
JSON_OUT = BASE / "test_files/"

UID = "2CCI3BkwKdqM4wOOwB5xRRxvOha"
FINGERPRINT = "8fa23329efa65477f077d99e145e4087190a55cc"

PARAMS = {
    "git_repo": "https://gitlab.com/Linaro/lkft/mirrors/stable/linux-stable-rc",
    "git_ref": "master",
    "target_arch": "x86_64",
    "toolchain": "gcc-12",
    "kconfig": "tinyconfig",
}
JSON_DATA = {
    "empty": "no_real_values",
    "uid": "1234",
    "git_repo": "https://gitlab.com/no_real_repo",
    "git_ref": "master",
    "git_sha": "6fae37b8a05e58b6103198e89d12dc0d6d472d92",
    "git_describe": "test-rc",
}
JSON_BUILD_DATA = {
    "state": "provisioning",
    "result": "None",
    "uid": "1234",
    "git_repo": "https://gitlab.com/no_real_repo",
    "git_ref": "master",
    "git_describe": "test-rc",
}

JSON_RESPONSE = """{
"count":1,
"version": "example_branch_with_additional_values",
"git_sha":"1234",
"tux_fingerprint":"8fa23329efa65477f077d99e145e4087190a55cc",
"results":[
{
"metadata":"https://www.example_metadata.pl",
"id":1234
}
]
}"""


@mock.patch("tuxtrigger.tuxintegration.subprocess.run")
@mock.patch("tempfile.NamedTemporaryFile")
def test_tux__build_call(mock_temp_file, mock_run, tux_config, squad_group_good):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "master", "stable_plan", "example_project", None, None, None
    )
    test_tux = TuxSuiteIntegration(True, test_branch, tux_config)
    build = MockedStdout(returncode=0, stdout=JSON_DATA)
    mock_run.return_value = build
    with open(BASE / "test_files/test.json", "r") as temp_file:
        mock_temp_file.return_value.__enter__.return_value = temp_file
        result = test_tux.tux_build_call(**PARAMS)
    assert result.uid == JSON_DATA["uid"]

    build_error = MockedStdout(returncode=1, stdout="", stderr="Tuxsuite Failure")
    mock_run.return_value = build_error
    with pytest.raises(TuxsuiteException) as exc:
        test_tux.tux_build_call(**PARAMS)
    assert "Tuxsuite not build repo" in str(exc)


@mock.patch(
    "tuxtrigger.tuxintegration.subprocess.run",
    side_effect=TuxsuiteException("*** Tuxsuite not build repo"),
)
def test_tux_build_call_error(mock_run, squad_group_good, tux_config):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "master", "stable_plan", "example_project", None, None, None
    )
    test_tux = TuxSuiteIntegration(True, test_branch, tux_config)
    build = MockedStdout(returncode=1, stdout=None)
    mock_run.return_value = build
    with pytest.raises(TuxsuiteException) as ex:
        test_tux.tux_build_call(**PARAMS)
    assert "Tuxsuite not build" in str(ex.value)


@mock.patch("tuxtrigger.tuxintegration.subprocess.run")
@mock.patch("tempfile.NamedTemporaryFile")
def test_tux_plan_call(
    mock_temp_file, mock_run, squad_group_good, tux_config, tmp_path
):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "master", "stable_plan", "example_project", None, None, None
    )
    test_tux = TuxSuiteIntegration(True, test_branch, tux_config)

    build_err = MockedStdout(returncode=1, stdout=JSON_DATA)
    mock_run.return_value = build_err
    with pytest.raises(TuxtriggerException) as exc_tuxtrigger:
        test_tux.tux_plan_call(
            None,
        )

    assert "*** Not able to submit plan" in str(exc_tuxtrigger)
    with pytest.raises(TuxsuiteException) as exc_tuxsuite:
        test_tux.tux_plan_call(
            JSON_DATA,
        )
    assert "Submitting Plan for master_test-rc failed" in str(exc_tuxsuite)

    build = MockedStdout(returncode=0, stdout=JSON_DATA)
    mock_run.return_value = build
    test_tux.tux_plan_call(JSON_DATA)
    mock_run.assert_called_with(
        [
            "tuxsuite",
            "plan",
            "--git-repo",
            "https://gitlab.com/no_real_repo",
            "--git-ref",
            "master",
            "--name",
            "test-rc",
            "--no-wait",
            BASE / "stable_plan",
            "--json-out",
            mock_temp_file().__enter__().name,
            "--callback",
            "https://dummy-qa-reports.org/api/fetchjob/~non.existing/example_project/test-rc/env/tuxsuite.com",
            "--parameters",
            "SQUAD_URL=https://dummy-qa-reports.org/api/submit/~non.existing/example_project/test-rc/env/",
        ]
    )

    test_tux.branch_object.lab = "test_lab"
    test_tux.branch_object.lava_test_plans_project = "test_lava_project"
    test_tux.tux_plan_call(JSON_DATA)
    mock_run.assert_called_with(
        [
            "tuxsuite",
            "plan",
            "--git-repo",
            "https://gitlab.com/no_real_repo",
            "--git-ref",
            "master",
            "--name",
            "test-rc",
            "--no-wait",
            BASE / "stable_plan",
            "--json-out",
            mock_temp_file().__enter__().name,
            "--callback",
            "https://dummy-qa-reports.org/api/fetchjob/~non.existing/example_project/test-rc/env/tuxsuite.com",
            "--parameters",
            "SQUAD_URL=https://dummy-qa-reports.org/api/submit/~non.existing/example_project/test-rc/env/",
            "--lab",
            "test_lab",
            "--lava-test-plans-project",
            "test_lava_project",
        ]
    )


@mock.patch("tuxtrigger.tuxintegration.subprocess.run")
def test_build_result(mock_run, tux_config, squad_group_good):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "master", "stable_plan", "example_project", None, None, None
    )
    test_tux = TuxSuiteIntegration(True, test_branch, tux_config)
    test_tux.uid = UID
    build = MockedStdout(returncode=0, stdout=json.dumps(JSON_BUILD_DATA))
    mock_run.return_value = build
    json_output = test_tux.build_result()
    mock_run.assert_called_once_with(
        ["tuxsuite", "build", "get", test_tux.uid, "--json"],
        stdout=-1,
        stderr=-1,
        text=True,
    )
    build = MockedStdout(returncode=1, stdout="Oops!")
    mock_run.return_value = build
    with pytest.raises(TuxsuiteException) as exc:
        test_tux.build_result()
    assert "*** Build result for UID:2CCI3BkwKdqM4wOOwB5xRRxvOha failed" in str(exc)

    test_tux.uid = None
    assert test_tux.build_result() is None
    assert JSON_BUILD_DATA == json_output


@mock.patch("tuxtrigger.tuxintegration.pre_tux_run")
@mock.patch("tuxtrigger.tuxintegration.Branch.check_squad_project")
@mock.patch("tuxtrigger.tuxintegration.Branch.configure_squad_client")
@mock.patch("tuxtrigger.tuxintegration.TuxSuiteIntegration.tux_build_call")
@mock.patch("tuxtrigger.tuxintegration.Branch.compare_sha")
def test_tuxsuite_trigger(
    mock_change,
    mock_tux_build,
    mock_squad_config,
    mock_squad_project,
    mock_custom_script,
    squad_group_good,
    tux_config,
):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "master", "stable_plan", "example_project", None, None, None
    )
    test_branch.input_dict = {}

    mock_change.return_value = True
    tux_config.pre_submit_path = BASE
    tuxsuite_trigger(tux_config, test_branch)
    mock_squad_config.assert_called()
    mock_squad_project.assert_called()
    mock_tux_build.assert_called()
    mock_custom_script.assert_called()

    tux_config.submit_mode = "always"
    tuxsuite_trigger(tux_config, test_branch)
    mock_tux_build.assert_called()
    tux_config.submit_mode = "never"
    result = tuxsuite_trigger(tux_config, test_branch)
    assert result is None


@mock.patch("tuxtrigger.tuxintegration.TuxSuiteIntegration.build_result")
@mock.patch("tuxtrigger.tuxintegration.TuxSuiteIntegration.tux_plan_call")
def test_tux_plan_submitter(mock_plan, mock_build, tux_config, squad_group_good):
    test_repo = Repository("not_existing_url", squad_group_good)
    test_branch = Branch(
        test_repo, "master", "stable_plan", "example_project", None, None, None
    )
    test_tux = TuxSuiteIntegration(True, test_branch, tux_config)
    test_tux.uid = UID

    assert tux_plan_submitter(tux_config, None) is None

    mock_build.return_value = JSON_BUILD_DATA
    tux_plan_submitter(tux_config, [test_tux])
    mock_plan.assert_called()

    tux_config.disable_squad = True
    tux_plan_submitter(tux_config, [test_tux])
    assert tux_config.json_out == Path(".")
    assert test_tux.branch_object.repository.squad_group is None
