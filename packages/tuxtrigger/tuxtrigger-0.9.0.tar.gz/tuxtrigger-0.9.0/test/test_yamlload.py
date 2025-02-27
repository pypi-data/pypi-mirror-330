#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT


from pathlib import Path

from tuxtrigger.yamlload import yaml_file_read

BASE = (Path(__file__) / "..").resolve()

ERROR_PATH = BASE / "./test_files/error_path.yaml"
HAPPY_PATH = BASE / "./test_files/happy_path.yaml"

READED_CONFIG = {
    "repositories": [
        {
            "branches": [
                {
                    "name": "not_existing_branch",
                    "plan": "stable.yaml",
                    "squad_project": "example_project",
                },
                {
                    "name": "also_doesn't exist",
                    "plan": "stable-next.yaml",
                    "squad_project": "example_project",
                },
            ],
            "squad_group": "~non.existing",
            "url": "http://not_existing_path/repository.git",
        }
    ]
}


def test_yaml_file_read():
    assert type(yaml_file_read(HAPPY_PATH)) == dict
    assert type(yaml_file_read(ERROR_PATH)) == dict
    assert yaml_file_read(ERROR_PATH) == READED_CONFIG
