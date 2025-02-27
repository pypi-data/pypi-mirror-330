#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TIMEOUT = 60


def _get_session(retries: int):
    session = requests.Session()

    retry_strategy = Retry(
        total=retries,
        status_forcelist=[408, 413, 429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "DELETE", "PUT", "TRACE"],
        backoff_factor=1,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def requests_get(*args, **kwargs) -> requests.Response:
    session = _get_session(retries=10)
    return session.get(*args, timeout=TIMEOUT, **kwargs)


def requests_post(*args, **kwargs) -> requests.Response:
    session = _get_session(retries=0)
    return session.post(*args, timeout=TIMEOUT, **kwargs)
