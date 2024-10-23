#!/usr/bin/env python3

from datetime import datetime, date, timedelta
from os import getenv
from sqlalchemy.orm import Session

from api.tempo_day import TempoAPI
from models.day import Day
from models.pricing import Pricing
from utils.dbconn import get_session


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
            add_day(db_session, api_day)

        db_session.commit()


def add_day(session: Session, day: dict):
    pricing: Pricing | None = (
        session.query(Pricing)
        .filter(
            Pricing.color == day.get("codeJour"), Pricing.period == day.get("periode")
        )
        .first()
    )

    if pricing:
        day_exist: Day | None = (
            session.query(Day).filter(Day.date == day.get("dateJour")).first()
        )

        if not day_exist:

            day = Day(
                date=day.get("dateJour"),
                id_pricing=pricing.id,
            )
            session.add(day)
