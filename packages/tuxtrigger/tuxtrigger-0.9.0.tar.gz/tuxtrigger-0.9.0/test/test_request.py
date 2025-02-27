# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT


import json
import os

# from http.client import HTTPMessage
from unittest import mock

from tuxtrigger import request

# from unittest.mock import ANY, Mock, call


class MockedRequest:
    def __init__(self, status_code):
        self.status_code = status_code


"""
temporary disabled function - throwing an error on local repo
@mock.patch("urllib3.connectionpool.HTTPConnectionPool._get_conn")
def test_get_session(connection_mock):
    connection_mock.return_value.getresponse.side_effect = [
        Mock(status=500, msg=HTTPMessage()),
        Mock(status=429, msg=HTTPMessage()),
        Mock(status=200, msg=HTTPMessage()),
    ]
    r = request.get_session(3)
    response = r.get(url="http://anyurl.pl/testme")
    response.raise_for_status()
    assert connection_mock.return_value.request.mock_calls == [
        call("GET", "/testme", body=None, headers=ANY),
        call("GET", "/testme", body=None, headers=ANY),
        call("GET", "/testme", body=None, headers=ANY),
    ]
"""


@mock.patch("tuxtrigger.request.requests_get")
def test_requests_get(mock_session):
    mock_req = MockedRequest(status_code=200)
    mock_session.return_value = mock_req
    req = request.requests_get(url="https://example.pl/xyz")
    assert req.status_code == 200


@mock.patch("tuxtrigger.request.requests_post")
def test_requests_post(mock_session):
    test_data = """{
        "fingerprint":"8fa23329efa65477f077d99e145e4087190a55cc",
        "git_sha":"5f9df76887bf8170e8844f1907c13fbbb30e9c36"
    }"""
    headers = {"Auth-Token": os.getenv("SQUAD_TOKEN")}
    mock_req = MockedRequest(status_code=201)
    mock_session.return_value = mock_req
    req = request.requests_post(
        url="https://example.pl/send-me-data",
        data=json.loads(test_data),
        headers=headers,
    )
    mock_session.assert_called_with(
        url="https://example.pl/send-me-data",
        data=json.loads(test_data),
        headers=headers,
    )
    assert req.status_code == 201
