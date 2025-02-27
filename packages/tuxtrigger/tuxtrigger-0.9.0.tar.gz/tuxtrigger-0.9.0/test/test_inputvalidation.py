#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from pathlib import Path
from types import GeneratorType

import pytest

from tuxtrigger.exceptions import TuxtriggerException
from tuxtrigger.inputvalidation import TuxtriggerConfiguration, YamlValidator
from tuxtrigger.storage import YamlStorage

READED_DATA = {
    "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git": [
        "1",
        "2",
        "3",
        "4",
    ],
}


def test_yaml_validator():
    test_url = YamlValidator("https://linaro.org/", "test_group", []).url_path()
    assert test_url.netloc == "linaro.org"

    with pytest.raises(TypeError) as exc:
        YamlValidator("www.linaro.org", "test_group", [])
        assert "Invalid url input" in str(exc)


def test_tuxtrigger_configuration(tux_config, tux_config_kernel):
    assert isinstance(tux_config_kernel.storage_class, YamlStorage)
    del tux_config.config_dict["config"]
    assert tux_config.create_squad_config() is None

    config_generator = tux_config.create_repo_list()
    assert isinstance(config_generator, GeneratorType)
    assert isinstance(next(config_generator), YamlValidator)


def test_tuxtrigger_configuration_error(tux_config_kernel):
    del tux_config_kernel.config_dict["repositories"]
    with pytest.raises(TuxtriggerException) as exc:
        next(tux_config_kernel.create_repo_list())
        assert "Data input is none" in str(exc)


def test_tuxtrigger_configuration_error_plan(tux_config_kernel):
    with pytest.raises(TuxtriggerException) as exc:
        TuxtriggerConfiguration(tux_config_kernel, Path("notExisting/Path/"), Path())
    assert "Plan Path does not exist, check Plan dir" in str(exc)


def test_configure_callback_headers():
    test_headers = "test"
    with pytest.raises(TuxtriggerException) as exc:
        TuxtriggerConfiguration({}, Path("/"), Path("/"), callback_headers=test_headers)
    assert "Callback should be formatted as `header:value`" in str(exc)

    test_headers = "first: 1, second: 2"
    test_config = TuxtriggerConfiguration(
        {}, Path("/"), Path("/"), callback_headers=test_headers
    )
    assert (
        "'CALLBACK_HEADERS': { 'first': ' 1',' second': ' 2' }"
        in test_config.squad_config["settings"]
    )


def test_supress_build(tux_config_kernel):
    test_repository = tux_config_kernel.create_repo_list()

    tux_config_kernel.submit_mode = "always"
    assert tux_config_kernel.suppress_build(next(test_repository), READED_DATA) is True
    test_repository = tux_config_kernel.create_repo_list()

    tux_config_kernel.submit_mode = "never"
    readed_data = {}
    assert tux_config_kernel.suppress_build(next(test_repository), readed_data) is False
