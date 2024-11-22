#!/usr/bin/env python3

from datetime import datetime, date, timedelta
from os import getenv
from sqlalchemy.exc import IntegrityError

from api.tempo_day import TempoAPI
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
        days: list = db_session.query(Day).all()
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
        except Exception as e:
            get_logger().error(e)


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
