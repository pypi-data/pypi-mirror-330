#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import subprocess
from pathlib import Path

from tuxtrigger import __version__

BASE = (Path(__file__) / "../..").resolve()


def test_setup_parser():
    version_result = subprocess.run(
        ["sh", f"{BASE}/run", "-v"], stdout=subprocess.PIPE, text=True
    )
    help_result = subprocess.run(
        ["sh", f"{BASE}/run", "--help"], stdout=subprocess.PIPE, text=True
    )
    assert f"TuxTrigger, {__version__}" in version_result.stdout
    assert (
        "usage: TuxTrigger [-h] [--output OUTPUT] [--pre-submit PRE_SUBMIT]"
        in help_result.stdout
    )
