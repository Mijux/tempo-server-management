#!/usr/bin/env python3

from datetime import datetime, date, timedelta
from os import getenv
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.tempo_day import TempoAPI
from api.tasmota import TastomaAPI, TastomaStubAPI
from models.day import Day
from models.pricing import Pricing
from utils.dbconn import get_session
from utils.exceptions import DBPricingDoesNotExistError, DBDayAlreadyExistsError
from utils.logger import get_logger


def init_day_table():
    START_SERVER_DATE = getenv("START_SERVER_DATE", "2024-06-01")
    start_date = datetime.strptime(START_SERVER_DATE, "%Y-%m-%d").date()
    today_date = date.today()

    with get_session() as db_session:
        days: List = db_session.query(Day).all()
        if len(days) == 0:
            get_logger().warning("Day table has not been initialized")

    date_list = []
    date_itetator = start_date
    while date_itetator <= today_date:
        date_list.append(date_itetator.strftime("%Y-%m-%d"))
        date_itetator += timedelta(days=1)

    all_days_from_start = TempoAPI().get_days(date_list)

    for api_day in all_days_from_start:
        try:
            add_day(api_day)
        except:
            pass


# This function is used to fill days where we dont retrieve tasmota data
def init_fill_power_consumption():
    with get_session() as db_session:

        power_total = None
        if getenv("ENVIRONMENT", None).upper() == "PROD":
            power_total = TastomaAPI().get_power_total()
        else:
            power_total = TastomaStubAPI().get_power_total()

        days_filled: list[Day] = (
            db_session.query(Day)
            .filter(
                or_(Day.consumption_offpeak != None, Day.consumption_fullpeak != None)
            )
            .all()
        )

        power_total_registered = 0
        for day_filled in days_filled:
            if day_filled.consumption_offpeak:
                power_total_registered += day_filled.consumption_offpeak
            if day_filled.consumption_fullpeak:
                power_total_registered += day_filled.consumption_fullpeak

        power_to_dispatch = power_total - power_total_registered

        days_to_fill: list[Day] = (
            db_session.query(Day)
            .filter(
                or_(Day.consumption_offpeak == None, Day.consumption_fullpeak == None),
                Day.date < date.today().strftime("%Y-%m-%d"),
            )
            .all()
        )

        if len(days_to_fill) == 0:
            return

        average_power_per_day = power_to_dispatch / len(days_to_fill)

        for day_to_fill in days_to_fill:
            if not day_to_fill.consumption_offpeak:
                day_to_fill.consumption_offpeak = average_power_per_day * 1 / 3
                power_to_dispatch -= day_to_fill.consumption_offpeak

            if not day_to_fill.consumption_fullpeak:
                day_to_fill.consumption_fullpeak = average_power_per_day * 2 / 3
                power_to_dispatch -= day_to_fill.consumption_fullpeak

        get_logger().info(f"{abs(round(power_to_dispatch,4))} were not dispatched")

        try:
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise DBError(e)


# This function is ised to fill day where tasmota data are missing. The power calculated is the average of all other days
def fill_missing_consumption():
    pass


def add_day(day: dict):
    with get_session() as db_session:
        pricing: Pricing | None = (
            db_session.query(Pricing)
            .filter(
                Pricing.color == day.get("codeJour"),
                Pricing.period == day.get("periode"),
            )
            .first()
        )

        if pricing:
            new_day = Day(
                date=day.get("dateJour"),
                id_pricing=pricing.id,
            )
            db_session.add(new_day)

            try:
                db_session.commit()
            except IntegrityError:
                db_session.rollback()
                raise DBDayAlreadyExistsError(day.get("dateJour"))

        else:
            raise DBPricingDoesNotExistError(day.get("codeJour"), day.get("periode"))
