#!/usr/bin/env python3

from datetime import datetime, date
from os import getenv
from utils.enums.period import PeriodE

from db.dao.user import get_user
from db.dao.consumption import get_consumption


class Stats:

    @staticmethod
    def get_user_state(user_id: str, period: int):
        """
        if period is global:
            => return the total value from START_SERVER_DATE (check .env file)
            => return the total per year
            => return the number of derogation on global
        if period is year:
            => return the total value from 1 january
            => return the total per month from january
            => return the number of derogation on the current year
        if period is month:
            => return the total value from 1st of month
            => return the total per week from 1st of month
            => return the number of derogation on the current month
        if period is week:
            => return the total value from the 1st day of week (Monday 6am to Monday 6am)
            => return the total per day from the 1st day of week
            => return the number of derogation on the current week
        if period is yesterday:
            => return the total value of day-1
            => return the total per hour of the day-1
        if period is today:
            => return the total value of day-1
            => return the total per hour of the day-1
        """
        period_e = PeriodE.from_number(period)

        if not period_e:
            return None  # Here should be an exception

        if not get_user(user_id):
            return None  # Here should be an exception

        if period_e is PeriodE.GLOBAL:
            return Stats.get_global()

    @staticmethod
    def get_user_derogation_state(user_id: str, period: int):
        pass

    @staticmethod
    def get_global():
        ret = {}

        start_date_str = getenv("START_SERVER_DATE")
        end_date_str = date.today().strftime("%Y-%m-%d")

        start_consumption = get_consumption(start_date_str)
        end_consumption = get_consumption(end_date_str)

        ret["total"] = (
            end_consumption.end_consumption_power
            - start_consumption.begin_consumption_power
        )

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        for i in range(start_date.year - end_date.year):
            pass
