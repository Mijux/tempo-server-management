#!/usr/bin/env python3

from enum import Enum


class PeriodE(Enum):
    GLOBAL = 0
    YEAR = 1
    MONTH = 2
    WEEK = 3
    YESTERDAY = 4
    TODAY = 5

    @classmethod
    def from_number(cls, number: int):
        try:
            return cls(number)
        except:
            return None
