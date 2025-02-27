#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

from tuxtrigger.repository import Repository
from tuxtrigger.storage import Storage, YamlStorage

BASE = (Path(__file__) / "..").resolve()
TEST_PATH = BASE / "test_files/gitsha.yaml"

READED_DATA = {
    "https://git.kernel.org/pub/scm/linux/kernel/git/tomba/linux.git": {
        "fingerprint": "8fa23329efa65477f077d99e145e4087190a55cc",
        "for-laurent": {"ref": "refs/for-laurent", "sha": "12345"},
        "master": {"ref": "refs/master/torvalds", "sha": "12345"},
    },
    "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git": {
        "fingerprint": "eb054f9048d6a8c3de909d97cf7ae080662f591c",
        "master": {"ref": "refs/master/torvalds", "sha": "1234567"},
        "v5.19": {"ref": "refs/v5.19", "sha": "12345"},
    },
}


def test_storage_implementation():
    class Storage_impl(Storage):
        pass

    with pytest.raises(NotImplementedError):
        Storage_impl(TEST_PATH).read_stored_data()

    with pytest.raises(NotImplementedError):
        Storage_impl(TEST_PATH).write_data()


def test_read_stored_data(tmp_path):
    assert YamlStorage(TEST_PATH).read_stored_data() == READED_DATA
    assert YamlStorage(tmp_path / "not_existing.yaml").read_stored_data() is None


def test_write_data(tmp_path):
    with tmp_path / "not_existing_file.yaml" as storage:
        test_write_object = YamlStorage(storage)
        test_write_object.storage_data = READED_DATA
        test_write_object.write_data()
        assert test_write_object.read_stored_data() == READED_DATA


def test_update_storage_data(tmp_path, squad_group_good):
    test_repository_kernel = Repository(
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
        squad_group_good,
    )
    test_repository_kernel.fingerprint = "1234"

    storage_class = YamlStorage(tmp_path / "not_existing.yaml")
    storage_class.read_stored_data()
    assert storage_class.storage_data == {}

    storage_class.update_storage_data(None, test_repository_kernel)
    assert storage_class.storage_data == {
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git": {
            "fingerprint": "1234"
        }
    }

    test_repository_kernel2 = Repository(
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux-next.git",
        squad_group_good,
    )
    test_repository_kernel2.fingerprint = "12345678"
    storage_class.update_storage_data(READED_DATA, test_repository_kernel2)
    assert storage_class.storage_data == {
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git": {
            "fingerprint": "1234"
        },
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux-next.git": {
            "fingerprint": "12345678"
        },
    }

    test_repository_kernel2.fingerprint = "1234567890"
    storage_class.update_storage_data(READED_DATA, test_repository_kernel2)
    assert storage_class.storage_data == {
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git": {
            "fingerprint": "1234"
        },
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux-next.git": {
            "fingerprint": "1234567890"
        },
    }
    storage_class = YamlStorage(TEST_PATH)
    storage_class.read_stored_data()

    storage_class.update_storage_data(READED_DATA, test_repository_kernel2)
    assert storage_class.storage_data == {
        "https://git.kernel.org/pub/scm/linux/kernel/git/tomba/linux.git": {
            "fingerprint": "8fa23329efa65477f077d99e145e4087190a55cc",
            "for-laurent": {"sha": "12345", "ref": "refs/for-laurent"},
            "master": {"sha": "12345", "ref": "refs/master/torvalds"},
        },
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git": {
            "fingerprint": "eb054f9048d6a8c3de909d97cf7ae080662f591c",
            "master": {"sha": "1234567", "ref": "refs/master/torvalds"},
            "v5.19": {"sha": "12345", "ref": "refs/v5.19"},
        },
        "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux-next.git": {
            "fingerprint": "1234567890"
        },
    }
