#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxtrigger.exceptions import (
    InvalidArgument,
    SquadException,
    TuxsuiteException,
    TuxtriggerException,
)


def test_tux_trig_exception():
    exc = TuxtriggerException("test message")
    assert isinstance(exc, Exception) is True
    assert exc.__str__() == "test message"


def test_inheritance():
    arg_exc = InvalidArgument()
    tux_exc = TuxsuiteException()
    squad_exc = SquadException()
    assert isinstance(arg_exc, TuxtriggerException) is True
    assert isinstance(tux_exc, TuxtriggerException) is True
    assert isinstance(squad_exc, TuxtriggerException) is True
