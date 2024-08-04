#!/usr/bin/env python3

from requests import get as rget
from re import match
from os.path import join


class TempoAPI:

    HOST = "https://www.api-couleur-tempo.fr/api"
    JOUR = "jourTempo"
    JOURS = "joursTempo"

    DATE_REGEX = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"

    def get_day(date: str) -> dict | None:
        if match(TempoAPI.DATE_REGEX, date):
            url = join(TempoAPI.HOST, TempoAPI.JOUR, date)
            req = rget(url)

            if req.status_code == 200:
                return req.json()

            else:
                print(f"Error when retrieve {url}")
        else:
            print(f"date must be in YYYY-MM-DD format, currently date was : {date}")

    def get_days(dates: list[str]) -> list | None:
        url = join(TempoAPI.HOST, TempoAPI.JOURS) + "?"
        for date in dates:
            if match(TempoAPI.DATE_REGEX, date):
                url += f"dateJour[]={date}&"
            else:
                print(f"date must be in YYYY-MM-DD format, currently date was : {date}")
                return None

        url = url[:-1]
        req = rget(url)

        if req.status_code == 200:
            return req.json()
        else:
            print(f"Error when retrieve {url}")
