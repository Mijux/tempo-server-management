#!/usr/bin/env python3

from json import load
from models.pricing import Pricing
from os import getenv
from sqlalchemy.orm import Session

from utils.dbconn import get_session


def init_pricing_table():
    POWER_PRICE_PATH = getenv("POWER_PRICE", "ressources/power_price.json")

    with get_session() as db_session:
        pricings: List = db_session.query(Pricing).all()

        if len(pricings) == 0:
            print("> Pricing table has not been initialized")

        with open(POWER_PRICE_PATH) as f:
            power_price = load(f)
            for period in power_price:
                print(f"\t- Checking value for period {period}")

                for day_color in power_price[period]:
                    add_pricing(
                        db_session, day_color, power_price[period][day_color], period
                    )

        db_session.commit()


def add_pricing(session: Session, color: str, color_price: dict, period: str):
    pricing = (
        session.query(Pricing)
        .filter(Pricing.color == color, Pricing.period == period)
        .first()
    )

    if pricing:
        pricing.hc = color_price["hc"]
        pricing.hp = color_price["hp"]

    else:
        p = Pricing(
            color=color,
            period=period,
            hc=color_price["hc"],
            hp=color_price["hp"],
        )
        session.add(p)
