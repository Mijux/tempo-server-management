#!/usr/bin/env python3

from json import load
from models.pricing import Pricing
from os import getenv
from sqlalchemy.orm import Session

from utils.dbconn import get_session


def init_table():
    POWER_PRICE_PATH = getenv("POWER_PRICE", "ressources/power_price.json")

    with get_session() as db_session:
        pricings: List = db_session.query(Pricing).all()

        if len(pricings) == 0:
            print("> Table has not been initialized")

        with open(POWER_PRICE_PATH) as f:
            power_price = load(f)
            for period in power_price:
                print(f"\t- Checking value for period ending at {period}")

                for day in power_price[period]:
                    add_pricing(db_session, day, power_price[period][day], period)

        db_session.commit()


def add_pricing(session: Session, color: str, color_price: dict, period_end):
    pricing = (
        session.query(Pricing)
        .filter(Pricing.color == color, Pricing.period_end == period_end)
        .first()
    )

    if pricing:
        pricing.hc = color_price["hc"]
        pricing.hp = color_price["hp"]

    else:
        p = Pricing(
            color=color,
            period_end=period_end,
            hc=color_price["hc"],
            hp=color_price["hp"],
        )
        session.add(p)
