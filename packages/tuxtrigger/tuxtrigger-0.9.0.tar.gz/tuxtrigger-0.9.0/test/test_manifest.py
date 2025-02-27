#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import json
from pathlib import Path
from unittest import mock

import pytest

from tuxtrigger.exceptions import TuxtriggerException
from tuxtrigger.manifest import git_manifest_download, git_repository_fingerprint

BASE = (Path(__file__) / "..").resolve()

FINGERPRINT = "c8f105f060651674a38b2103190f2ca52381ce76"

REPO_URL = "https://git.kernel.org/pub/dummy/repo.git"
MANIFEST_REPO = "/pub/scm/linux/kernel/git/wwguy/iwlwifi.git"


class RequestMock:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content


@mock.patch("tuxtrigger.manifest.requests_get")
def test_git_manifest_download(mock_req):
    with open(BASE / "test_files/manifest.js.gz", "rb") as test_file:
        manifest = RequestMock(status_code=200, content=test_file.read())
        mock_req.return_value = manifest
        output = git_manifest_download()
    assert isinstance(json.loads(output), dict)


@mock.patch("tuxtrigger.manifest.requests_get")
def test_git_manifest_not_found(mock_req):
    manifest = RequestMock(status_code=404, content=None)
    mock_req.return_value = manifest
    with pytest.raises(TuxtriggerException) as ex:
        git_manifest_download()
    assert "TuxTrigger not able to download manifest 404" in str(ex.value)


@mock.patch("tuxtrigger.manifest.requests_get")
def test_git_repository_fingerprint(mock_manifest):
    with open(BASE / "test_files/manifest.js.gz", "rb") as test_file:
        manifest = RequestMock(status_code=200, content=test_file.read())
        mock_manifest.return_value = manifest
        output = git_manifest_download()
    test_fingerprint = git_repository_fingerprint(output, MANIFEST_REPO)
    assert test_fingerprint == FINGERPRINT
    with pytest.raises(KeyError) as exc:
        git_repository_fingerprint(output, "REPO_URL")
    assert "Tracked Repository does not exist in manifest" in str(exc)
