#!/usr/bin/env python3

from json import load
from db.models.pricing import Pricing
from os import getenv
from sqlalchemy.exc import IntegrityError

from utils.dbconn import get_session
from utils.exceptions import DBPricingInsertionError
from utils.logger import get_logger


def init_pricing_table():
    POWER_PRICE_PATH = getenv("POWER_PRICE", "ressources/power_price.json")

    with get_session() as db_session:
        pricings: list = db_session.query(Pricing).all()

        if len(pricings) == 0:
            get_logger().warning("Pricing table has not been initialized")

    with open(POWER_PRICE_PATH) as f:
        power_price = load(f)
        for period in power_price:
            get_logger().info(f"Checking value for period {period}")

            for day_color in power_price[period]:
                add_pricing(day_color, power_price[period][day_color], period)


def add_pricing(color: str, color_price: dict, period: str):
    with get_session() as db_session:
        princing: Pricing | None = (
            db_session.query(Pricing)
            .filter(Pricing.color == color, Pricing.period == period)
            .first()
        )

        if princing:
            princing.price_fullpeak = color_price["fullpeak"]
            princing.price_offpeak = color_price["offpeak"]
        else:
            new_pricing = Pricing(
                period=period,
                color=color,
                price_fullpeak=color_price["fullpeak"],
                price_offpeak=color_price["offpeak"],
            )
            db_session.add(new_pricing)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise DBPricingInsertionError(color, period)
