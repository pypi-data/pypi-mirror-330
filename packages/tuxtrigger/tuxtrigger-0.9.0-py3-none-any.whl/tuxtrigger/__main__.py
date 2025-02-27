#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import logging
import sys

from tuxtrigger.argparser import setup_parser
from tuxtrigger.configparser import create_dynamic_configuration, present_created_config
from tuxtrigger.exceptions import TuxtriggerException
from tuxtrigger.inputvalidation import TuxtriggerConfiguration
from tuxtrigger.repository import Branch, Repository
from tuxtrigger.tuxintegration import tux_plan_submitter, tuxsuite_trigger
from tuxtrigger.utils import get_manifest, setup_logger

LOG = logging.getLogger("tuxtrigger")


def main() -> int:
    parser = setup_parser()
    options = parser.parse_args()
    setup_logger(options.log_file, options.log_level)

    try:
        config = create_dynamic_configuration(options.config)
        LOG.info(f"Imported configuration file {options.config}")
        if options.generate_config:
            LOG.info("Presenting loaded configuration")
            return present_created_config(config)
        config_instance_loaded = TuxtriggerConfiguration(
            config_dict=config,
            plan_path=options.plan,
            storage_path=options.output,
            pre_submit_path=options.pre_submit,
            submit_mode=options.submit,
            json_out=options.json_out,
            disable_plan=options.disable_plan,
            disable_squad=options.disable_squad,
            callback_url=options.callback_url,
            callback_headers=options.callback_headers,
            private=options.private,
        )
        stored_data = config_instance_loaded.storage_class.read_stored_data()
        tuxsuite_obj_list = list()
        LOG.info("Configuration loaded successfully")
        manifest_json = get_manifest(config_instance_loaded)
        for tracked_repository in config_instance_loaded.create_repo_list():
            repository = Repository(
                tracked_repository.url, tracked_repository.squad_group
            )
            LOG.info(f"* Repository: {repository}")
            repository.load_fingerprint(manifest_json)

            if repository.check_fingerprint(
                stored_data
            ) and not config_instance_loaded.suppress_build(
                tracked_repository, stored_data
            ):
                LOG.info("Builds suppressed")
                continue

            config_instance_loaded.storage_class.update_storage_data(
                stored_data, repository
            )

            for tracked_branch in tracked_repository.branches:
                branch = Branch(
                    repository,
                    tracked_branch["name"],
                    tracked_branch["plan"],
                    tracked_branch["squad_project"],
                    tracked_branch.get("lab"),
                    tracked_branch.get("lava_test_plans_project"),
                    stored_data,
                )
                LOG.info(f"** Branch: {branch}")

                tuxcall_object = tuxsuite_trigger(
                    config_instance_loaded,
                    branch,
                )
                if tuxcall_object:
                    tuxsuite_obj_list.append(tuxcall_object)
                config_instance_loaded.storage_class.storage_data[
                    repository.repository_url
                ].update(branch.stored_data)
            config_instance_loaded.storage_class.write_data()
        LOG.info("** Enter Submitting Plans Phase **")
        while tuxsuite_obj_list and not config_instance_loaded.disable_plan:
            tuxcall_object = tux_plan_submitter(
                config_instance_loaded, tuxsuite_obj_list
            )
            if tuxcall_object is not None:
                tuxsuite_obj_list.remove(tuxcall_object)

        LOG.info("Submitting Plans Phase Completed")
        LOG.info(f"Saving fingerprint/SHA values to {options.output}")

        LOG.info("Tuxtrigger run finished")
        return 0
    except TuxtriggerException as e:
        parser.error(str(e))


def start() -> None:
    if __name__ == "__main__":
        sys.exit(main())


start()
