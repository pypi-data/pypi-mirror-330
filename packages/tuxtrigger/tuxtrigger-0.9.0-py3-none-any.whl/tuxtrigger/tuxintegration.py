#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
import urllib3
from pathlib import Path

from tuxtrigger.constants import BUILD_PARAMS, JSON_PATH
from tuxtrigger.exceptions import TuxsuiteException, TuxtriggerException
from tuxtrigger.inputvalidation import TuxtriggerConfiguration
from tuxtrigger.repository import Branch
from tuxtrigger.utils import pre_tux_run

LOG = logging.getLogger("tuxtrigger")


class TuxSuiteIntegration:
    def __init__(
        self,
        repository_changed: bool,
        branch_object: Branch,
        config_object: TuxtriggerConfiguration,
    ):
        self.repository_changed = repository_changed
        self.branch_object = branch_object
        self.config_object = config_object

    def tux_build_call(self, **build_params) -> TuxSuiteIntegration:
        with tempfile.NamedTemporaryFile(suffix=".json") as json_temp:
            cmd = [
                "tuxsuite",
                "build",
                "--git-repo",
                self.branch_object.repository.repository_url,
                "--git-ref",
                self.branch_object.branch,
                "--target-arch",
                build_params.get("target_arch", "x86_64"),
                "--kconfig",
                build_params.get("kconfig", "tinyconfig"),
                "--toolchain",
                build_params.get("toolchain", "gcc-12"),
                "--json-out",
                json_temp.name,
                "--no-wait",
            ]

            if self.config_object.private:
                cmd.append("--private")

            build = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if build.returncode != 0:
                LOG.warning(f"*** Build stdout {build.stdout}")
                LOG.warning(f"*** Build stderr {build.stderr}")
                raise TuxsuiteException(f"*** Tuxsuite not build repo {build.stderr}")

            LOG.debug(f"\t{build.stdout}")
            json_output = json.load(json_temp)
            self.uid = json_output.get("uid")
            LOG.debug(f'\tBuild UID: {json_output["uid"]}')
            LOG.info(f"\tBuild submitted for {self.branch_object.branch}")
            return self

    def tux_plan_call(
        self,
        json_data: dict,
    ) -> int:
        if json_data is None:
            LOG.warning("*** Not able to submit plan -> json output is None")
            raise TuxtriggerException(
                "*** Not able to submit plan -> json output is None"
            )
        with tempfile.NamedTemporaryFile(suffix=".json") as json_temp:
            cmd = [
                "tuxsuite",
                "plan",
                "--git-repo",
                json_data["git_repo"],
                "--git-ref",
                json_data["git_ref"],
                "--name",
                json_data["git_describe"],
                "--no-wait",
                self.config_object.plan_path / self.branch_object.plan,
                "--json-out",
                json_temp.name,
            ]

            if self.config_object.private:
                LOG.debug("\t enable private builds")
                cmd.append("--private")

            if not self.config_object.disable_squad:
                LOG.debug("\tcallback option enabled")
                cmd.append("--callback")
                cmd.append(
                    f"{os.getenv('SQUAD_HOST')}/api/fetchjob/{self.branch_object.repository.squad_group}/{self.branch_object.squad_project}/{json_data['git_describe']}/env/tuxsuite.com"
                )
                cmd.append("--parameters")
                cmd.append(
                    f"SQUAD_URL={os.getenv('SQUAD_HOST')}/api/submit/{self.branch_object.repository.squad_group}/{self.branch_object.squad_project}/{json_data['git_describe']}/env/"
                )

            if self.branch_object.lab:
                LOG.debug("\tlab option enabled")
                cmd.append("--lab")
                cmd.append(self.branch_object.lab)

            if self.branch_object.lava_test_plans_project:
                LOG.debug("\tlava_test_plans_project option enabled")
                cmd.append("--lava-test-plans-project")
                cmd.append(self.branch_object.lava_test_plans_project)

            plan = subprocess.run(cmd)

            if plan.returncode != 0:
                LOG.warning(
                    f'*** Submitting Plan for {json_data["git_ref"]}_{json_data["git_describe"]} failed'
                )
                raise TuxsuiteException(
                    f'*** Submitting Plan for {json_data["git_ref"]}_{json_data["git_describe"]} failed'
                )
            if (
                self.config_object.json_out
                or self.branch_object.repository.squad_group is None
            ):
                LOG.debug("\tjson_out option enabled")
                try:
                    shutil.copy(
                        json_temp.name,
                        self.config_object.json_out
                        / f'{json_data["git_ref"]}_{json_data["git_describe"]}.json',
                    )

                    LOG.info(
                        f'\tJson file for git_describe: {json_data["git_describe"]} saved'
                    )
                except TuxtriggerException as exc:
                    LOG.warning(
                        f'*** Json file for git_describe: {json_data["git_describe"]} not saved: {str(exc)}'
                    )
            if not self.config_object.disable_squad:
                LOG.debug("\tSQUAD enabled")
                self.branch_object.squad_submit_tuxsuite(
                    json_data, Path(json_temp.name)
                )
                if self.config_object.callback_url:
                    self.branch_object.register_squad_callback(
                        json_data, self.config_object.callback_url
                    )
            LOG.info(f'\tSubmitting Plan for {json_data["git_describe"]}')
            return 0

    def build_result(self) -> dict | None:
        if self.uid is None:
            return None
        build = subprocess.run(
            ["tuxsuite", "build", "get", self.uid, "--json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if build.returncode != 0:
            LOG.warning(f"*** Build result for UID:{self.uid} failed")
            raise TuxsuiteException(f"*** Build result for UID:{self.uid} failed")
        json_output = json.loads(build.stdout)
        LOG.debug(f"\tJSON OUTPUT: {json_output}")
        LOG.debug(
            f'\tBuild {json_output["uid"]} state: {json_output["state"]}, result: {json_output["result"]}, git describe: {json_output["git_describe"]}'
        )
        LOG.info(
            f'\tRepo: {self.branch_object.repository.repository_url}, branch: {self.branch_object.branch}, git describe: {json_output["git_describe"]}'
        )
        return json_output


def tuxsuite_trigger(
    config_object: TuxtriggerConfiguration, branch_object: Branch
) -> TuxSuiteIntegration | None:
    repo_changed = branch_object.compare_sha()
    branch_object.update_stored_data()
    if config_object.submit_mode == "never":
        repo_changed = False
        LOG.info("\tBuild suspended")
    elif config_object.submit_mode == "always":
        repo_changed = True
        LOG.info("\tExecuting build")
    else:
        LOG.info(f"\tBuild changed: {repo_changed}")

    if repo_changed:
        if config_object.pre_submit_path:
            LOG.info("Invoking custom script")
            pre_tux_run(
                config_object.pre_submit_path,
                branch_object,
                repo_changed,
            )
        if not config_object.disable_squad:
            try:
                branch_object.configure_squad_client()
                branch_object.check_squad_project(config_object.squad_config)
            except urllib3.exceptions.ResponseError as e:
                LOG.debug(f"SQUAD connection error: {e}")
        LOG.info("\t Proceed to submit tuxbuild")
        return TuxSuiteIntegration(
            repo_changed, branch_object, config_object
        ).tux_build_call(**BUILD_PARAMS)
    LOG.info("\tNot a single build was triggered")
    return None


def tux_plan_submitter(
    config_object: TuxtriggerConfiguration, tuxsuite_obj_list: list
) -> TuxSuiteIntegration | None:
    if tuxsuite_obj_list is None:
        return None
    for tuxsuite_obj in tuxsuite_obj_list:
        time.sleep(10)
        if config_object.disable_squad:
            tuxsuite_obj.branch_object.repository.squad_group = None
            if config_object.json_out is None:
                config_object.json_out = JSON_PATH
        json_build_output = tuxsuite_obj.build_result()
        if json_build_output["git_describe"] is not None:
            LOG.debug(f"\tUID: {tuxsuite_obj.uid}")
            LOG.debug(f"\tPlan file name: {tuxsuite_obj.branch_object.plan}")
            LOG.info("\tProceed to submit tuxplan")
            tuxsuite_obj.tux_plan_call(json_build_output)
            return tuxsuite_obj
    return None
