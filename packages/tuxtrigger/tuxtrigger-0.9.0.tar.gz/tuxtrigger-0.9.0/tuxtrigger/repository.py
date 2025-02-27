#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from squad_client.commands.submit_tuxsuite import SubmitTuxSuiteCommand
from squad_client.core.api import SquadApi
from squad_client.core.models import Squad
from squad_client.shortcuts import create_or_update_project, register_callback

from tuxtrigger.exceptions import SquadException, TuxtriggerException
from tuxtrigger.manifest import git_repository_fingerprint

LOG = logging.getLogger("tuxtrigger")


class Repository:
    def __init__(self, repository_url: str, squad_group: str):
        self.repository_url = repository_url
        self.squad_group = squad_group

    def load_fingerprint(self, manifest_json: bytes):
        repository_parsed = urlparse(self.repository_url.rstrip("/"))
        self.fingerprint = ""
        if "git.kernel.org" in repository_parsed.netloc:
            self.fingerprint = git_repository_fingerprint(
                manifest_json, repository_parsed.path
            )

    def check_fingerprint(self, archive_data: dict | None) -> bool:
        if archive_data is None:
            LOG.warning("\t*** Data Input is none, not able to compare fingerprint")
            LOG.debug(f"\tfingerprint: {self.fingerprint}")
            return False
        if "fingerprint" not in archive_data.get(self.repository_url, ""):
            LOG.warning("\t*** Fingerprint not found in yaml file")
            LOG.debug(f"\tRepo name: {self.repository_url}")
            return False
        old_fingerprint = archive_data[self.repository_url]["fingerprint"]
        if not self.fingerprint == old_fingerprint:
            LOG.info(
                f"\tfingerprint: {self.fingerprint} vs \
            previous fingerprint {old_fingerprint}"
            )
            return False
        LOG.info(f"\tfingerprint: {self.fingerprint}")
        LOG.info("\tno changes")
        return True

    def __str__(self):
        return self.repository_url


class Branch:
    def __init__(
        self,
        repository: Repository,
        branch: str,
        plan: str,
        squad_project: str,
        lab: str | None,
        lava_test_plans_project: str | None,
        stored_data: dict = {},
    ):
        self.repository = repository
        self.branch = branch
        self.plan = plan
        self.squad_project = squad_project
        self.lab = lab
        self.lava_test_plans_project = lava_test_plans_project
        self.stored_data = stored_data

    def get_sha_value(self) -> dict:
        value_dict = dict()
        git_result = subprocess.run(
            ["git", "ls-remote", self.repository.repository_url, self.branch],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        splited_value = git_result.stdout.split()
        value_dict[self.branch] = {"sha": "", "ref": ""}
        if git_result.returncode != 0:
            return value_dict

        if splited_value:
            self.sha_value = splited_value[0]
            value_dict[self.branch] = {"sha": splited_value[0], "ref": splited_value[1]}
        LOG.debug(f"** Branch: {self.branch} ls-remote output: {value_dict}")
        return value_dict

    def compare_sha(self) -> bool:
        self.input_dict = self.get_sha_value()
        if not self.stored_data or not self.stored_data.get(
            self.repository.repository_url, ""
        ):
            LOG.warning("\t*** Data Input is none, not able to compare sha")
            LOG.debug(f'\tsha: {self.input_dict[self.branch]["sha"]}')
            return True
        if self.branch not in self.stored_data.get(self.repository.repository_url, ""):
            LOG.warning("\t*** Branch not found in yaml file")
            LOG.debug(f"\tbranch name: {self.branch}")
            return True
        if (
            not self.input_dict[self.branch]["sha"]
            == self.stored_data[self.repository.repository_url][self.branch]["sha"]
        ):
            LOG.info(
                f'\tsha: {self.input_dict[self.branch]["sha"]} vs \
            previous sha {self.stored_data[self.repository.repository_url][self.branch]["sha"]}'
            )
            return True
        LOG.info(f'\tsha: {self.input_dict[self.branch]["sha"]}')
        LOG.info("\tno changes")
        return False

    def update_stored_data(self):
        if self.stored_data is None:
            self.stored_data = {}
        self.stored_data = {self.branch: self.input_dict.get(self.branch)}

    def configure_squad_client(self):
        SquadApi.configure(url=os.getenv("SQUAD_HOST"), token=os.getenv("SQUAD_TOKEN"))

    def check_squad_project(self, squad_project_config: dict | None = {}) -> str:
        group = Squad().group(self.repository.squad_group)
        if group is None:
            LOG.warning(
                f"*** SQUAD response error - group {self.repository.squad_group} not found"
            )
            raise SquadException(
                f"*** SQUAD response error - group {self.repository.squad_group} not found"
            )

        project, err = create_or_update_project(
            group_slug=self.repository.squad_group,
            slug=self.squad_project,
            name=self.squad_project,
            overwrite=True,
            **squad_project_config,
        )
        LOG.info(f"\tProject {self.squad_project} Exists!, parsing id {project.id}")
        self.squad_project_id = project.id
        return self.squad_project_id

    def squad_submit_tuxsuite(self, json_data: dict, json_plan: Path) -> bool:
        if self.repository.squad_group is None or self.squad_project is None:
            LOG.warning("*** SQUAD config is not available! Unable to process")
            raise TuxtriggerException(
                "*** SQUAD config is not available! Unable to process"
            )

        args = type("", (), {})()
        args.group = self.repository.squad_group
        args.project = self.squad_project
        args.build = json_data["git_describe"]
        args.backend = "tuxsuite.com"
        args.json = json_plan
        args.fetch_now = False

        LOG.info("\tProceed SQUAD tuxsuite submit")
        return SubmitTuxSuiteCommand().run(args)

    def register_squad_callback(self, json_data: dict, callback_url: str):
        if self.repository.squad_group is None or self.squad_project is None:
            LOG.warning("*** SQUAD config is not available! Unable to process")
            raise TuxtriggerException(
                "*** SQUAD config is not available! Unable to prsocess"
            )

        callback, err = register_callback(
            group_slug=self.repository.squad_group,
            project_slug=self.squad_project,
            build_version=json_data["git_describe"],
            url=callback_url,
            record_response=True,
        )
        LOG.info("\tSQUAD callback registered")
        if callback is None:
            LOG.warning(
                f"*** SQUAD response error - not able to register callback for {callback_url}, {err}"
            )
            raise SquadException(
                f"*** SQUAD response error - not able to register callback for {callback_url}, {err}"
            )

    def __str__(self):
        return self.branch
