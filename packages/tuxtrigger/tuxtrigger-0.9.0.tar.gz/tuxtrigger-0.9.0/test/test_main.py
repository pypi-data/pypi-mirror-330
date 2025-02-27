#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import json
import sys
from pathlib import Path

import pytest
import yaml

import tuxtrigger.__main__ as main_module
from tuxtrigger.repository import Branch, Repository
from tuxtrigger.tuxintegration import TuxSuiteIntegration

BASE = (Path(__file__) / "../..").resolve()

MANIFEST_JSON = {
    "/pub/scm/linux/kernel/git/tomba/linux.git": {
        "owner": "Tomi Valkeinen",
        "description": "Tomi Valkeinen's kernel tree",
        "modified": 1660133218,
        "reference": "/pub/scm/linux/kernel/git/paulg/4.8-rt-patches.git",
        "fingerprint": "8fa23329efa65477f077d99e145e4087190a55cc",
        "forkgroup": "af9f4487-d538-46e5-b148-e18dfb461f8a",
        "head": "ref: refs/heads/master",
    },
    "/pub/scm/linux/kernel/git/torvalds/linux.git": {
        "symlinks": ["/pub/scm/linux/kernel/git/torvalds/linux-2.6.git"],
        "description": "Linux kernel source tree",
        "reference": "/pub/scm/linux/kernel/git/paulg/4.8-rt-patches.git",
        "modified": 1661194011,
        "fingerprint": "2c8d80ee6d795dc6951bbdef466ef19c64ff717d",
        "owner": "Linus Torvalds",
        "head": "ref: refs/heads/master",
        "forkgroup": "af9f4487-d538-46e5-b148-e18dfb461f8a",
    },
}

CREATED_CONFIG = {
    "repositories": [
        {
            "url": "https://git.kernel.org/pub/scm/linux/kernel/git/tomba/linux.git",
            "squad_group": "~non.existing",
            "branches": [
                {
                    "name": "master",
                    "squad_project": "example_project",
                    "plan": "stable.yaml",
                },
                {
                    "name": "for-laurent",
                    "squad_project": "example_project",
                    "plan": "stable-next.yaml",
                },
            ],
        },
        {
            "url": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
            "squad_group": "~non.existing",
            "branches": [
                {
                    "name": "master",
                    "squad_project": "example_project",
                    "plan": "stable.yaml",
                },
                {
                    "name": "v5.19",
                    "squad_project": "example_project",
                    "plan": "stable-next.yaml",
                },
            ],
        },
    ]
}


@pytest.fixture
def argv():
    return ["tuxtrigger"]


@pytest.fixture(autouse=True)
def patch_argv(monkeypatch, argv):
    monkeypatch.setattr(sys, "argv", argv)


class TestMain:
    def test_start(self, monkeypatch, mocker):
        monkeypatch.setattr(main_module, "__name__", "__main__")
        main = mocker.patch("tuxtrigger.__main__.main", return_value=1)
        exit = mocker.patch("sys.exit")
        main_module.start()
        main.assert_called()
        exit.assert_called_with(1)

    def test_main_version(self, argv, capsys):
        argv.append("-v")
        with pytest.raises(SystemExit):
            main_module.main()
        out, out_err = capsys.readouterr()
        assert "TuxTrigger" in out

    def test_main_key_error(self, argv):
        argv.extend([f"{BASE}/test/test_files/error_path.yaml"])
        with pytest.raises(SystemExit):
            main_module.main()
            assert main_module.main() == 1

    def test_main_generate_config(self, argv, capsys, mocker, monkeypatch):
        argv.append(f"{BASE}/test/test_files/happy_path.yaml")
        argv.append("--generate-config")
        monkeypatch.setattr(main_module, "__name__", "__main__")
        main_generate_config = mocker.patch(
            "tuxtrigger.__main__.create_dynamic_configuration",
            return_value=CREATED_CONFIG,
        )
        main_module.main()
        main_generate_config.assert_called()
        stdout, stderr = capsys.readouterr()
        assert (
            yaml.dump(CREATED_CONFIG, default_flow_style=False, sort_keys=False)
            in stdout
        )

    def test_main_run(
        self, argv, capsys, mocker, monkeypatch, tux_config_kernel, tmp_path
    ):
        output_file = tmp_path / "output.yaml"
        log_file = tmp_path / "log.txt"
        test_repository = Repository(
            "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git", None
        )
        test_branch = Branch(
            test_repository,
            "master",
            "stable.yaml",
            "example_project",
            None,
            None,
            stored_data={"master": {"sha": "1234", "ref": "master"}},
        )
        test_tuxintegration = (
            TuxSuiteIntegration(True, test_branch, tux_config_kernel),
        )

        argv.append(f"{BASE}/test/test_files/happy_path2.yaml")
        argv.append(f"--plan={BASE}/test/test_files/")
        argv.append("--submit=always")
        argv.append(f"--log-file={log_file}")
        argv.append(f"--output={output_file}")
        monkeypatch.setattr(main_module, "__name__", "__main__")
        main_manifest = mocker.patch(
            "tuxtrigger.__main__.get_manifest", return_value=json.dumps(MANIFEST_JSON)
        )
        main_tuxsuite_object = mocker.patch(
            "tuxtrigger.__main__.tuxsuite_trigger",
            return_value=test_tuxintegration,
        )
        main_branch_obj = mocker.patch(
            "tuxtrigger.__main__.Branch", return_value=test_branch
        )
        main_tuxplan_object = mocker.patch(
            "tuxtrigger.__main__.tux_plan_submitter",
            return_value=test_tuxintegration,
        )
        print(main_tuxsuite_object)
        main_module.main()
        main_manifest.assert_called()
        main_tuxsuite_object.assert_called()
        main_branch_obj.assert_called()
        main_tuxplan_object.assert_called()
