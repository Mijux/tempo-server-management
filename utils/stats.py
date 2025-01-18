#!/usr/bin/env python3

from datetime import datetime, date, timedelta
from os import getenv

from pytz import timezone
from db.dao.day import get_day, get_days_with_derogations
from db.dao.pricing import get_pricing
from db.dao.user_presence_status import UserPresenceStatusDao
from db.models.day import Day
from utils.dbconn import get_session
from utils.enums.period import PeriodE

from db.dao.user import get_user
from db.dao.consumption import (
    get_consumption,
    get_consumption_by_period,
    get_last_entry_for_year,
    get_first_entry_for_year,
)
from db.dao.derogation import (
    get_derogation_per_user,
    get_derogation_users,
    get_derogations,
)


class Stats:

    @staticmethod
    def get_user_state(user_id: str, period: int):
        """
        used for /get_my_state and /get_state <user_id>

        {
            "server": {
                consumption: 100,
                price: 10
            },
            "user": {
                consumption: 30,
                price: 3,
                derogation: {
                    number_of_derog: 2,
                    consumption: 5,
                    price: 2
                }
            }
        }

        """
        period_e = PeriodE.from_number(period)

        if not period_e:
            return None  # Here should be an exception

        if not get_user(user_id):
            return None  # Here should be an exception

        tz = timezone(getenv("TIMEZONE"))

        start_date = None
        end_date = None

        if period_e is PeriodE.GLOBAL:
            start_date = getenv("START_SERVER_DATE")
            end_date = datetime.now(tz=tz).strftime("%Y-%m-%d")
        elif period_e is PeriodE.YEAR:
            curr = datetime.now(tz=tz)
            start_date = f"{curr.year}-01-01"
            end_date = datetime.now(tz=tz).strftime("%Y-%m-%d")
        elif period_e is PeriodE.MONTH:
            curr = datetime(tz=tz)
            start_date = f"{curr.year}-{curr.month}-01"
            end_date = datetime.now(tz=tz).strftime("%Y-%m-%d")
        elif period_e is PeriodE.WEEK:
            end_date = datetime.now(tz=tz).strftime("%Y-%m-%d")
            start_date = end_date + timedelta(days=-end_date.weekday())
        elif period_e is PeriodE.YESTERDAY:
            start_date = datetime.now(tz=tz) + timedelta(days=-1)
            end_date = start_date
        elif period_e is PeriodE.TODAY:
            start_date = datetime.now(tz=tz)
            end_date = start_date
        else:
            pass

        ret = {}
        ret["server"]["price"], ret["server"]["consumption"] = (
            Stats.compute_power_and_price_between_dates(start_date, end_date)
        )
        ret["user"]["price"], ret["user"]["consumption"] = (
            Stats.compute_user_power_and_price_between_dates(
                start_date, end_date, user_id
            )
        )

        (
            ret["user"]["derogation"]["number_of_derog"],
            ret["user"]["derogation"]["price"],
            ret["user"]["derogation"]["consumption"],
        ) = Stats.compute_user_derogation_power_and_price_between_dates(
            user_id, start_date, end_date
        )

        return ret

    @staticmethod
    def compute_user_derogation_power_and_price_between_dates(
        start_date: str, end_date: str, user_id: str
    ):
        derogations = get_derogation_per_user(user_id, start_date, end_date)

        nb_of_derog = len(derogations)
        total_price = 0
        total_power = 0

        for derogation in derogations:
            r = Stats.compute_power_price_day(derogation.date)
            nb_users_on_derogation = len(get_derogation_users(derogation.date))

            total_price += r[0] / nb_users_on_derogation
            total_power += r[1]

        return (nb_of_derog, total_price, total_power)

    @staticmethod
    def compute_power_and_price_between_dates(start_date: str, end_date: str) -> float:
        sdate = datetime.strptime(start_date, "%Y-%m-%d")
        edate = datetime.strptime(end_date, "%Y-%m-%d")

        total_price = 0
        total_power = 0

        loop_date = sdate
        while loop_date <= edate:
            r = Stats.compute_power_price_day(loop_date.strftime("%Y-%m-%d"))
            total_price += r[0]
            total_power += r[1]

        return (total_price, total_power)

    @staticmethod
    def compute_power_price_day(date: str):
        tz = timezone(getenv("TIMEZONE"))
        day = get_day(date, with_consumption=True)
        pricing = get_pricing(day.id_pricing)

        total_price = 0
        total_power = 0

        for consumption in day.consumptions:
            shour = datetime.fromtimestamp(consumption.begin_hour, tz)

            kwh_price = None
            if shour.hour >= 6 and shour.hour < 22:
                kwh_price = pricing.price_fullpeak
            else:
                kwh_price = pricing.price_offpeak

            total_price += kwh_price * abs(
                consumption.end_consumption_power - consumption.begin_consumption_power
            )
            total_power += abs(
                consumption.end_consumption_power - consumption.begin_consumption_power
            )

        return (total_price, total_power)

    @staticmethod
    def compute_user_power_and_price_between_dates(
        start_date: str, end_date: str, user_id: str
    ):
        presence_periods = UserPresenceStatusDao.get_user_presences(
            user_id, start_date, end_date
        )
        tz = timezone(getenv("TIMEZONE"))

        total_price = 0
        total_power = 0

        for period in presence_periods:
            consumptions = get_consumption_by_period(
                period.arrival_date, period.leave_date
            )

            total_consumption_price = 0
            total_consumption_power = 0

            for consumption in consumptions:
                day = get_day(consumption.date)
                pricing = get_pricing(day.id_pricing)

                shour = datetime.fromtimestamp(consumption.begin_hour, tz)

                kwh_price = None
                if shour.hour >= 6 and shour.hour < 22:
                    kwh_price = pricing.price_fullpeak
                else:
                    kwh_price = pricing.price_offpeak

                total_consumption_price += kwh_price * abs(
                    consumption.end_consumption_power
                    - consumption.begin_consumption_power
                )
                total_consumption_power += abs(
                    consumption.end_consumption_power
                    - consumption.begin_consumption_power
                )

            total_price += total_consumption_price
            total_power += total_consumption_power

        return (total_price, total_power)
