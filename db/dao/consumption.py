#!/usr/bin/env python3

from datetime import datetime, timedelta
from os import getenv
from pytz import timezone
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound


from api.tasmota import TastomaAPI, TastomaStubAPI
from utils.dbconn import get_session
from utils.logger import get_logger
from db.models.consumption import Consumption
from db.models.day import Day


def init_consumption_table():
    tz = timezone(getenv("TIMEZONE"))

    with get_session() as db_session:
        days: list[Day] = db_session.query(Day).all()

        days_to_fill: list[Day] = []
        for day in days:
            if len(day.consumptions) == 0:
                days_to_fill.append(day)

    total_power_to_dispatch: float = None
    if getenv("ENVIRONMENT", None).upper() == "PROD":
        total_power_to_dispatch = TastomaAPI().get_power_total()
    else:
        total_power_to_dispatch = TastomaStubAPI().get_power_total()

    power_per_day = total_power_to_dispatch / len(days_to_fill)
    power_dispatched = 0

    loop_range = None
    last_day = None
    if datetime.now(tz).hour < 6:
        loop_range = days_to_fill[:-2]
        last_day = days_to_fill[-2]
    else:
        loop_range = days_to_fill[:-1]
        last_day = days_to_fill[-1]

    for day in loop_range:
        s_datetime = datetime.strptime(day.date, "%Y-%m-%d").replace(
            hour=6,
            minute=0,
            tzinfo=tz,
        )
        begin_timestamp = s_datetime.timestamp()
        end_timestamp = (s_datetime + timedelta(days=1)).timestamp()

        add_consumption(
            day.date,
            begin_timestamp,
            end_timestamp,
            power_dispatched,
            power_dispatched + power_per_day,
        )
        power_dispatched += power_per_day

    # For today, just fill to previous hour
    s_datetime = datetime.strptime(last_day.date, "%Y-%m-%d").replace(
        hour=6,
        minute=0,
        tzinfo=tz,
    )
    begin_timestamp = s_datetime.timestamp()
    end_timestamp = datetime.now(tz).timestamp()

    add_consumption(
        day.date,
        begin_timestamp,
        end_timestamp,
        power_dispatched,
        power_dispatched + power_per_day,
    )

    power_dispatched += power_per_day

    get_logger().info(f"A total of {total_power_to_dispatch} has been dispatched")
    get_logger().info(
        f"{abs(round(total_power_to_dispatch-power_dispatched))}kW/h were not dispatched"
    )


def add_consumption(
    date: str,
    begin_hour: int,
    end_hour: int,
    begin_consumption_power: float,
    end_consumption_power: float,
):
    with get_session() as db_session:
        new_consumption: Consumption = Consumption(
            date=date,
            begin_hour=int(begin_hour),
            end_hour=int(end_hour),
            begin_consumption_power=begin_consumption_power,
            end_consumption_power=end_consumption_power,
        )
        db_session.add(new_consumption)

        try:
            db_session.commit()
        except Exception as e:
            get_logger().error(e)


def get_consumption(date: str):
    with get_session() as db_session:
        try:
            return (
                db_session.query(Consumption).filter(Consumption.date == date).first()
            )
        except NoResultFound:
            return None