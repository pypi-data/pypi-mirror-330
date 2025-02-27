#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT
from pathlib import Path

MANIFEST_URL = "https://git.kernel.org/manifest.js.gz"

BUILD_PARAMS = {
    "git_repo": "",
    "git_ref": "",
    "target_arch": "x86_64",
    "toolchain": "gcc-12",
    "kconfig": "tinyconfig",
}

SQUAD_CONFIG = {
    "plugins": "linux_log_parser,ltp",
    "wait_before_notification_timeout": "600",
    "notification_timeout": "28800",
    "force_finishing_builds_on_timeout": "False",
    "important_metadata_keys": "build-url,git_ref,git_describe,git_repo,kernel_version",
    "thresholds": ["build/*-warnings"],
    "data_retention": "0",
    "is_public": "False",
}

JSON_PATH = Path("./")
