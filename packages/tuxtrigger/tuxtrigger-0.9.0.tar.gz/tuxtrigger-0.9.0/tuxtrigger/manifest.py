#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import gzip
import json
import logging
from io import BytesIO

from tuxtrigger.constants import MANIFEST_URL
from tuxtrigger.exceptions import TuxtriggerException
from tuxtrigger.request import requests_get

LOG = logging.getLogger("tuxtrigger")


def git_manifest_download() -> bytes:
    manifest_request = requests_get(MANIFEST_URL)

    if manifest_request.status_code != 200:
        LOG.warning(f"*** Manifest download error code {manifest_request.status_code}")
        raise TuxtriggerException(
            f"*** TuxTrigger not able to download manifest {manifest_request.status_code}"
        )

    LOG.debug(f"Manifest response {manifest_request.status_code}")

    with gzip.open(BytesIO(manifest_request.content), "rb") as gz_file:
        json_output = gz_file.read()

    return json_output


def git_repository_fingerprint(json_data: bytes, repo_url: str) -> str:
    json_parser = json.loads(json_data)
    if repo_url not in json_parser:
        raise KeyError(f"*** Tracked Repository does not exist in manifest {repo_url}")
    return json_parser[repo_url]["fingerprint"]
