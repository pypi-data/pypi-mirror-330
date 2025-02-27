#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import logging
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

from tuxtrigger.configparser import update_squad_config
from tuxtrigger.exceptions import SquadException, TuxtriggerException
from tuxtrigger.storage import YamlStorage

LOG = logging.getLogger("tuxtrigger")


class Base:
    def url_validation(self, url: str):
        urlScheme = urlparse(url)
        if urlScheme.scheme not in ["http", "https"]:
            raise TypeError("Invalid url input.")

    def url_path(self):
        return urlparse(self.url.rstrip("/"))


class TuxBase:
    def create_repo_list(self):
        if self.config_dict.get("repositories") is None:
            raise TuxtriggerException("Data input is none")
        for item in self.config_dict["repositories"]:
            yield YamlValidator(**item)

    def create_squad_config(self):
        if self.config_dict.get("squad_config", None) is None:
            return None
        return SquadConfigValidator(**self.config_dict["squad_config"])

    def configure_callback_headers(self):
        headers = []
        for element in self.callback_headers.split(","):
            items = element.split(":")
            if len(items) != 2:
                raise TuxtriggerException(
                    f'** Callback should be formatted as `header:value`, got "{items}" instead'
                )
            header, value = items
            headers.append(f"'{header}': '{value}'")

        return ",".join(headers)

    def suppress_build(self, tracked_repository, stored_data):
        if self.submit_mode in ["always", "never"]:
            LOG.info(f"Submit mode set to {self.submit_mode}")
        if (
            len(tracked_repository.branches)
            != len(stored_data.get(tracked_repository.url, [])) - 1
        ):
            LOG.info("Config file modification detected")
            return False
        return True

    def tux_keys_configure(self):
        tuxsuite_keys = subprocess.run(
            [
                "tuxsuite",
                "keys",
                "get",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if tuxsuite_keys.returncode != 0:
            LOG.warning("Not able to retrieve tuxkeys")
        tuxsuite_pubkey = None
        for line in tuxsuite_keys.stdout.splitlines():
            if line.startswith("ecdsa-sha2"):
                tuxsuite_pubkey = line
        return tuxsuite_pubkey


@dataclass
class YamlValidator(Base):
    url: str
    squad_group: str
    branches: List[Dict]
    regex: Optional[str] = None
    default_plan: Optional[str] = None
    default_lab: Optional[str] = None
    default_lava_test_plans_project: Optional[str] = None
    squad_project_prefix: Optional[str] = None
    default_squad_project: Optional[str] = None

    def __post_init__(self):
        self.url_validation(self.url)


@dataclass
class TuxtriggerConfiguration(TuxBase):
    config_dict: Dict
    plan_path: Path
    storage_path: Path
    pre_submit_path: Optional[Path] = None
    submit_mode: str = "change"
    json_out: Optional[Path] = None
    disable_plan: bool = False
    disable_squad: bool = False
    squad_config: Optional[dict] = field(default_factory=lambda: {})
    callback_url: Optional[str] = None
    callback_headers: Optional[str] = None
    sha_loop_dict: Dict = field(default_factory=lambda: {})
    private: bool = False
    is_public: bool = True

    def __post_init__(self):
        self.storage_class = YamlStorage(self.storage_path)
        if not self.disable_plan and not self.plan_path.exists():
            raise TuxtriggerException("Plan Path does not exist, check Plan dir")
        if self.disable_squad:
            return
        # Squad submission is not disabled, check for credentials
        self.check_squad_creds()
        self.squad_config = update_squad_config(self.create_squad_config())
        if self.callback_headers:
            self.squad_config[
                "settings"
            ] = f"{{ 'TUXSUITE_PUBLIC_KEY': '{self.tux_keys_configure()}', 'CALLBACK_HEADERS': {{ {self.configure_callback_headers()} }}}}"
        else:
            self.squad_config[
                "settings"
            ] = f"{{ 'TUXSUITE_PUBLIC_KEY': '{self.tux_keys_configure()}'}}"

    def check_squad_creds(self):
        squad_host, squad_token = os.getenv("SQUAD_HOST"), os.getenv("SQUAD_TOKEN")
        if squad_host and squad_token:
            urlScheme = urlparse(squad_host)
            if urlScheme.scheme not in ["http", "https"]:
                raise SquadException(
                    "Invalid 'SQUAD_HOST' environment variable url scheme, must start with 'http' or 'https'"
                )
        else:
            raise SquadException(
                "'SQUAD_HOST' and 'SQUAD_TOKEN' environment variables must be set"
            )


@dataclass
class SquadConfigValidator(Base):
    plugins: Optional[str] = None
    wait_before_notification_timeout: Optional[int] = None
    notification_timeout: Optional[int] = None
    force_finishing_builds_on_timeout: Optional[bool] = None
    important_metadata_keys: Optional[str] = None
    thresholds: Optional[str] = None
    data_retention: Optional[int] = None
    is_public: Optional[bool] = None
