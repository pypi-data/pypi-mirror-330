# Running TuxTrigger
## Prerequisites
* SQUAD account and SQUAD API token in `SQUAD_API` environment variable
* TuxSuite account and API token in `TUXSUITE_TOKEN` environment variable

## Create Configuration File

To make TuxTrigger work you have to provide configuration YAML file with declared SQUAD details and repositories data
(URL to tracked repository, selected branches and TuxSuite Plan file).

Example of basic TuxTrigger config file: `config.yaml`:

```yaml
repositories:
- url: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
  squad_group: ~pawel.szymaszek
  branches:
    - name: master
      squad_project: tuxtrigger-torvalds-v5.19
      plan: stable.yaml
    - name: v5.19-rc6
      squad_project: tuxtrigger-torvalds-v5.19
      plan: stable_next.yaml
      lava_test_plans_project: lkft
      lab: https://lkft.validation.linaro.org
```

TuxTrigger supports dynamic branch list generation with these parameters:

- `regex` - match branch names in selected repository using regexp
- `default_plan` - plan file name to be assigned for matched branches
- `squad_project_prefix` - prefix added to `squad_project` value in matched branches
- `default_squad_project` - default `squad_project` for matched branches
- `default_lava_test_plans_project` - Use to set value in matched branches
- `default_lab` - default LAVA URL for all matched branches
- `lab` - specify LAVA lab to use for jobs
- `lava_test_plans_project` - specifies project in lava-test-plans to use

```yaml
repositories:
- url: https://git.kernel.org/pub/scm/linux/kernel/git/arm64/linux.git
  squad_group: ~pawel.szymaszek
  regex: for-next/*
  default_plan: stable.yaml
  squad_project_prefix: generator
  default_lava_test_plans_project: lkft
  default_lab: https://lkft.validation.linaro.org
  branches:
  - name: for-next/acpi # hardcoded values won't be overwritten
    squad_project: generator-linux-for-next-acpi
    plan: stable_next.yaml
```

TuxTriggerer enables SQAUD project configuration. By setting values in TuxTrigger config file you are able to **create** or **update** SQUAD project.
In `config:` section you are able to specify one or more options:

```yaml
squad_config:
  plugins: linux_log_parser,ltp
  wait_before_notification_timeout: 600
  notification_timeout: 28800
  force_finishing_builds_on_timeout: False
  important_metadata_keys: build-url,git_ref,git_describe,git_repo,kernel_version
  thresholds: build/*-warnings
  data_retention: 0
repositories:
...
```
To check results of dynamically generated config use `--generate-config` argument.
Tuxtrigger will perform _dry-run_ and prompt generated config:

```shell
tuxtrigger /path/to/config.yaml --generate-config
```

## Create Plan for TuxSuite

:warning: TUXSUITE_TOKEN env variable must be set!

Create a TuxSuite plan and reference it in your configuration:

TuxSuite plan example, `my-plan.yml`:
```yaml
version: 1
name: stable_plan
description: stable_plan
jobs:
- tests:
    - {device: qemu-x86_64, tests: [ltp-smoke]}
```

For further information about plans and TuxSuite configuration please visit [TuxSuite Home](https://docs.tuxsuite.com/).

:warning: By default TuxTrigger takes plans from `share/plans` folder, but you can override it with argument `--plan=path/to/plans`:

```shell
tuxtrigger path/to/config.yaml --plan=path/to/plans
```

## Running TuxTrigger

To run TuxTrigger just launch the following command:
```shell
tuxtrigger /path/to/config.yaml
```
