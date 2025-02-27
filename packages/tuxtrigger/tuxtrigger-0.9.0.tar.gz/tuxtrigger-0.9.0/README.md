<div align="center">
  <img src="tuxtrigger.svg" alt="TuxTrigger Logo" width="40%" />
</div>

[![Pipeline Status](https://gitlab.com/Linaro/tuxtrigger/badges/main/pipeline.svg)](https://gitlab.com/Linaro/tuxtrigger/pipelines)
[![coverage report](https://gitlab.com/Linaro/tuxtrigger/badges/main/coverage.svg)](https://gitlab.com/Linaro/tuxtrigger/commits/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - License](https://img.shields.io/pypi/l/tuxtrigger)](https://gitlab.com/Linaro/tuxtrigger/blob/main/LICENSE)

[Documentation](https://linaro.gitlab.io/tuxtrigger) - [Repository](https://gitlab.com/Linaro/tuxtrigger) - [Issues](https://gitlab.com/Linaro/tuxtrigger/-/issues)

TuxTrigger, by [Linaro](https://www.linaro.org/), is a command line tool for controlling changes in repositories.  
TuxTrigger is a part of
[TuxSuite](https://tuxsuite.com), a suite of tools and services to help with
Linux kernel development.

[[_TOC_]]

# About TuxTrigger

TuxTrigger allows to automatically track a set of git repositories and branches. When a change occurs, TuxTrigger will build, test and track the results using Tuxsuite and SQUAD.

# Installing TuxTrigger

There are several options for using TuxTrigger:

- [From PyPI](install-pypi.md)
- [Run uninstalled](run-uninstalled.md)

# Using TuxTrigger

!!! note
    - TuxTrigger requires TuxSuite and SQUAD accounts (TuxSuite and SQUAD tokens).

To use TuxTrigger:

1. Create [TuxSuite](https://tuxsuite.com) account and provide TUXSUITE_TOKEN as environment variable.
2. Create [SQUAD](https://qa-reports.linaro.org/) account and provide SQUAD_TOKEN and SQUAD_HOST as environment variable.
Example:
```shell
SQUAD_HOST=https://qa-reports.linaro.org
```
3. Install TuxTrigger
4. [Create configuration.yaml file](docs/run.md#create-configuration-file)
5. Provide [plan.yaml](https://docs.tuxsuite.com/plan/) file(s) from [TuxSuite](https://tuxsuite.com)
6. Run TuxTrigger

Call tuxtrigger:

```shell
tuxtrigger /path/to/config.yaml --plan /path/to/plan_directory
```

Tuxtrigger will automatically start.
