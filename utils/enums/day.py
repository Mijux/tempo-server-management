#!/usr/bin/env python3

from enum import Enum


class DayE(Enum):
    UNKNOWN = 0
    BLUE = 1
    WHITE = 2
    RED = 3

    @classmethod
    def from_number(cls, number: int):
        return cls(number)
