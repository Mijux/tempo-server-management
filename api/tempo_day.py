#!/usr/bin/env python3

from requests import get as rget
from re import match
from os import getenv
from os.path import join

from utils.logger import get_logger


class TempoAPI:

    HOST = f"https://{getenv('HOST_TEMPO','www.api-couleur-tempo.fr')}/api"
    DAY = "jourTempo"
    DAYS = "joursTempo"

    DATE_REGEX = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"

    def get_day(date: str) -> dict | None:
        if match(TempoAPI.DATE_REGEX, date):
            url = join(TempoAPI.HOST, TempoAPI.DAY, date)
            req = rget(url)

            if req.status_code == 200:
                return req.json()

            else:
                get_logger().error(f"Can't retrieve {url}")
        else:
            get_logger().error(
                f"date must be in YYYY-MM-DD format, currently date was : {date}"
            )

        return None

    def get_days(dates: list[str]) -> list | None:
        url = join(TempoAPI.HOST, TempoAPI.DAYS) + "?"
        for date in dates:
            if match(TempoAPI.DATE_REGEX, date):
                url += f"dateJour[]={date}&"
            else:
                get_logger().error(
                    f"date must be in YYYY-MM-DD format, currently date was : {date}"
                )
                return None

        url = url[:-1]  # remove leading &
        req = rget(url)

        if req.status_code == 200:
            return req.json()
        else:
            get_logger().error(f"Can't retrieve {url}")
