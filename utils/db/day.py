#!/usr/bin/env python3


from models.day import Day
from models.pricing import Pricing
from utils.dbconn import get_session


def add_day(day: dict):

    with get_session() as db_session:
        pricing: Pricing | None = db_session.query(Pricing).filter(
            Pricing.color == day.codeJour, Pricing.period_end == day.periode
        )

        if pricing:
            day = Day(
                date=day.dateJour,
                id_pricing=pricing.id,
            )

            db_session.add(day)

        db_session.commit()
