#!/usr/bin/env python3

from datetime import datetime, date, timedelta
from os import getenv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.tempo_day import TempoAPI
from models.day import Day
from models.pricing import Pricing
from utils.dbconn import get_session
from utils.exceptions import DBPricingDoesNotExistError


def init_day_table():
    START_SERVER_DATE = getenv("START_SERVER_DATE", "2024-06-01")
    start_date = datetime.strptime(START_SERVER_DATE, "%Y-%m-%d").date()
    today_date = date.today()

    with get_session() as db_session:
        days: List = db_session.query(Day).all()
        if len(days) == 0:
            print("> Day table has not been initialized")

    date_list = []
    date_itetator = start_date
    while date_itetator <= today_date:
        date_list.append(date_itetator.strftime("%Y-%m-%d"))
        date_itetator += timedelta(days=1)

    all_days_from_start = TempoAPI().get_days(date_list)

    print(all_days_from_start)

    for api_day in all_days_from_start:
        add_day_old(api_day)


# This function is used to fill first first days where we dont retrieve tasmota data
def init_fill_power_consumption():
    pass


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
            db_session.add(day)

            try:
                db_session.commit()
            except IntegrityError:
                db_session.rollback()
                raise DBDayAlreadyExistsError(day.get("dateJour"))

        else:
            raise DBPricingDoesNotExistError(day.get("codeJour"), day.get("periode"))
