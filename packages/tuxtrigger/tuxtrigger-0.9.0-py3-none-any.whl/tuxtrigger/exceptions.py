#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT


class TuxtriggerException(Exception):
    def __str__(self):
        name = super().__str__()
        if hasattr(self, "msg"):
            return self.msg.format(name=name)
        else:
            return name


class InvalidArgument(TuxtriggerException):
    pass


class TuxsuiteException(TuxtriggerException):
    pass


class SquadException(TuxtriggerException):
    pass
