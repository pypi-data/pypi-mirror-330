#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import contextlib
import logging
from pathlib import Path

import yaml

from tuxtrigger.repository import Repository
from tuxtrigger.yamlload import yaml_file_read

LOG = logging.getLogger("tuxtrigger")


class Storage:
    def __init__(self, storage_localization: Path):
        self.storage_localization = storage_localization
        self.storage_data: dict = {}

    def read_stored_data(self):
        raise NotImplementedError("Subclasses should implement this method!")

    def write_data(self):
        raise NotImplementedError("Subclasses should implement this method!")


class YamlStorage(Storage):
    def read_stored_data(self) -> dict | None:  # type: ignore[return]
        output_file = (self.storage_localization).absolute()
        output_file.parent.mkdir(exist_ok=True)
        with contextlib.suppress(FileNotFoundError):
            readed_yaml_data = yaml_file_read(self.storage_localization)
            if readed_yaml_data is not None:
                self.storage_data.update(readed_yaml_data)
            return readed_yaml_data

    def write_data(self):
        with self.storage_localization.open("w") as writer:
            yaml.dump(
                self.storage_data, writer, default_flow_style=False, sort_keys=False
            )

    def update_storage_data(self, stored_data: dict, repository: Repository):
        if stored_data is None and not self.storage_data:
            self.storage_data = {
                repository.repository_url: {"fingerprint": repository.fingerprint}
            }
        elif stored_data is None or stored_data.get(repository.repository_url, True):
            self.storage_data.update(
                {repository.repository_url: {"fingerprint": repository.fingerprint}}
            )
        else:
            self.storage_data.update(stored_data)
