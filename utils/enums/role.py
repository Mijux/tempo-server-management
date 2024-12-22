#!/usr/bin/env python3

from enum import Enum


class RoleE(Enum):
    DEFAULT = 0
    ADMIN = 1


    @classmethod
    def from_number(cls, number: int):
        return cls(number)
