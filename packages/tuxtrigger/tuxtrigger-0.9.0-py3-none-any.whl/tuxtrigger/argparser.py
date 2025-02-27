#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT
import argparse
from pathlib import Path

from tuxtrigger import __version__

OUTPUT_FILE = Path("share/gitsha.yaml")
PLAN_PATH = Path("share/plans/")
LOG_FILE = Path("log.txt")


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="TuxTrigger",
        description="TuxTrigger command line tool for controlling changes in repositories",
    )
    parser.add_argument(
        "config", type=Path, help="config yaml file name", action="store"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="path for storing output file",
        action="store",
        default=OUTPUT_FILE,
    )
    parser.add_argument(
        "--pre-submit",
        type=Path,
        help="pre-tuxsuite script to run",
        action="store",
    )
    parser.add_argument(
        "--submit",
        "-s",
        type=str,
        help="trigger build on change",
        default="change",
        choices=["never", "change", "always"],
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="print log to file",
        default=LOG_FILE,
        action="store",
    )
    parser.add_argument(
        "--plan",
        type=Path,
        help="path to plan files",
        default=PLAN_PATH,
        action="store",
    )
    parser.add_argument(
        "--callback-url",
        type=str,
        help="Callback URL to post event on a plan execution",
        action="store",
    )
    parser.add_argument(
        "--callback-headers",
        type=str,
        help="Headers to be passed to callback-url",
        action="store",
    )

    parser.add_argument(
        "--log-level",
        "-l",
        type=str,
        help="set log level to more specific information",
        default="info",
        choices=["DEBUG", "INFO", "WARN", "ERROR"],
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        help="json output folder path",
        action="store",
    )
    parser.add_argument(
        "--disable-plan",
        help="disable submitting plan to tuxsuite",
        action="store_true",
    )
    parser.add_argument(
        "--disable-squad",
        help="disable submitting data to squad",
        action="store_true",
    )
    parser.add_argument(
        "--generate-config",
        help="dry-run to show generated config from regex value",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="prints current version",
        action="version",
        version=f"%(prog)s, {__version__}",
    )
    parser.add_argument(
        "-p",
        "--private",
        help="private options to be used with private repositories that need authentication. CAUTION: Please make sure the PAT token is added to tuxsuite.",
        action="store_true",
        default=False,
    )
    return parser
