#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import logging
import subprocess
import sys
from pathlib import Path
from urllib.parse import ParseResult, urlparse

import yaml

from tuxtrigger.constants import SQUAD_CONFIG as squad_config
from tuxtrigger.exceptions import TuxtriggerException
from tuxtrigger.yamlload import yaml_file_read

LOG = logging.getLogger("tuxtrigger")


def _run_lsremote_regex(repository: str, regex: str) -> dict:
    value_dict = dict()  # type: dict[str, str]
    git_result = subprocess.run(
        ["git", "ls-remote", "--refs", repository, regex],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if git_result.returncode != 0:
        return value_dict

    splited_value = git_result.stdout.split("\n")
    for value in splited_value:
        if len(value) > 1:
            temp_list = value.split("\t")
            branch_list = temp_list[1].split("/")
            branch = "/".join(branch_list[int(len(branch_list) / -2) :])  # noqa: E203
            value_dict[branch] = temp_list[0]
    return value_dict


def _create_squad_project(url: ParseResult, branch_name: str, prefix=None) -> str:
    url_fragment = (url.path).split("/")
    url_fragment = list(filter(None, url_fragment))
    if prefix is None:
        return f'{(url_fragment[-1]).replace(".git","")}-{branch_name.replace("/","-")}'
    return f'{prefix}-{(url_fragment[-1]).replace(".git","")}-{branch_name.replace("/","-")}'


def _check_default_values(yaml_data: dict) -> dict:
    for repository in yaml_data:
        default_squad_project = repository.get("default_squad_project", "")
        default_plan = repository.get("default_plan", "")
        default_lab = repository.get("default_lab", "")
        default_lava_test_plans_project = repository.get(
            "default_lava_test_plans_project", ""
        )
        for branch in repository.get("branches", []):
            if "plan" not in branch:
                branch["plan"] = default_plan
            if "squad_project" not in branch:
                branch["squad_project"] = default_squad_project
            if "lab" not in branch:
                branch["lab"] = default_lab
            if "lava_test_plans_project" not in branch:
                branch["lava_test_plans_project"] = default_lava_test_plans_project
    return yaml_data


def create_dynamic_configuration(yaml_path: Path) -> dict:
    if yaml_path is None:
        LOG.warning("*** Not able to generate data - config file not read")
        raise TuxtriggerException(
            "*** Not able to generate data - config file not read"
        )
    yaml_data = yaml_file_read(yaml_path)
    LOG.debug("Generating configuration")
    yaml_data["repositories"] = _check_default_values(yaml_data["repositories"])
    for repo in yaml_data["repositories"]:
        if "branches" not in repo.keys():
            repo["branches"] = []
        LOG.debug(f'Checking repository - {repo.get("url")}')
        if "regex" in repo:
            LOG.info(
                f'Regex value present in config - {repo["regex"]} , looking for branches'
            )
            git_branch_updated = _run_lsremote_regex(repo.get("url"), repo.get("regex"))
            for new_branch in git_branch_updated:
                if new_branch in str(repo["branches"]):
                    LOG.info(f"** Branch {new_branch} in config file, skip the branch")
                    continue
                repo["branches"].append(
                    {
                        "name": new_branch,
                        "squad_project": repo.get("default_squad_project")
                        or _create_squad_project(
                            urlparse(repo.get("url").rstrip("/")),
                            new_branch,
                            repo.get("squad_project_prefix"),
                        ),
                        "plan": repo.get("default_plan"),
                        "lab": repo.get("lab"),
                        "lava_test_plans_project": repo.get("lava_test_plans_project"),
                    }
                )
            LOG.info("Dynamic Config Generated")
    LOG.debug(f"updated yaml_data: {yaml_data}")
    return yaml_data


def present_created_config(created_config: dict) -> int:
    sys.stdout.write(
        yaml.dump(created_config, default_flow_style=False, sort_keys=False)
    )
    return 0


def update_squad_config(squad_object) -> dict:
    if squad_object is None:
        LOG.info("SQUAD config not available, processing default project config")
        return squad_config
    LOG.info("Updating SQUAD project configuration values")
    for key, value in squad_config.items():
        squad_validator_attribute = getattr(squad_object, key, None)
        if squad_validator_attribute is not None:
            squad_config[key] = str(squad_validator_attribute)
    return squad_config
