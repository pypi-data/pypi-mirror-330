#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import logging
import logging.handlers
import subprocess
import sys
from pathlib import Path

from tuxtrigger.exceptions import TuxtriggerException
from tuxtrigger.inputvalidation import TuxtriggerConfiguration
from tuxtrigger.manifest import git_manifest_download
from tuxtrigger.repository import Branch

LOG = logging.getLogger("tuxtrigger")


def setup_logger(log_file: Path, log_level: str):
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(logging.Formatter("[%(levelname)s] - %(message)s"))
    log_file_handler = logging.handlers.WatchedFileHandler(
        (log_file).absolute(),
        mode="w",
    )
    log_file_handler.setFormatter(logging.Formatter("[%(levelname)s] - %(message)s"))
    LOG.addHandler(log_handler)
    LOG.addHandler(log_file_handler)

    if log_level == "DEBUG":
        LOG.setLevel(logging.DEBUG)
    elif log_level == "WARN":
        LOG.setLevel(logging.WARNING)
    elif log_level == "ERROR":
        LOG.setLevel(logging.ERROR)
    else:
        LOG.setLevel(logging.INFO)


def get_manifest(config: TuxtriggerConfiguration) -> bytes:
    for repo in config.config_dict["repositories"]:
        if "git.kernel.org" in repo["url"].rstrip("/"):
            manifest_json = git_manifest_download()
            return manifest_json
    return b""


def pre_tux_run(
    script_path: Path,
    branch_object: Branch,
    repo_changed: bool,
):
    if script_path is None:
        LOG.warning("*** No script path provided")
        return
    if not repo_changed:
        LOG.warning("*** Repo not changed, Script not invoked")
        return
    new_sha = branch_object.stored_data.get(branch_object.branch, {})
    script_result = subprocess.run(
        [
            script_path,
            branch_object.repository.repository_url,
            branch_object.branch,
            new_sha.get("sha", ""),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if script_result.returncode != 0:
        LOG.warning("*** Script was not invoked properly")
        raise TuxtriggerException(
            f"*** Script was not invoked properly - {script_result.stderr}"
        )
    LOG.info(f"stdout: {script_result.stdout}")
    LOG.info(f"Script {script_path} performed astonishingly wonderful")
