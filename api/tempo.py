#!/usr/bin/env python3

from requests import get as rget
from re import match
from os import getenv
from os.path import join

from utils.logger import get_logger


class TempoAPI:

    HOST = None
    HOST_BASE_URL = None

    DAY = "jourTempo"
    DAYS = "joursTempo"

    API_DAY_DATE = "dateJour"
    API_DAY_COLOR_CODE = "codeJour"
    API_DAY_PERIOD = "periode"

    DATE_REGEX = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"

    def __init__(self):
        correct = True
        self.HOST = getenv("HOST_TEMPO", None)
        if not self.HOST:
            correct = False
            get_logger().error(
                "Please assign a value to HOST_TEMPO variable in your .env file"
            )

        self.HOST_BASE_URL = f"https://{self.HOST}/api"

        if not correct:
            exit(1)

    def get_day(self, date: str) -> dict | None:
        if match(TempoAPI.DATE_REGEX, date):
            url = join(self.HOST_BASE_URL, TempoAPI.DAY, date)
            req = rget(url)

            if req.status_code == 200:
                return self.translate(req.json())

            else:
                get_logger().error(f"Can't retrieve {url}")
        else:
            get_logger().error(
                f"date must be in YYYY-MM-DD format, currently date was : {date}"
            )

        return None

    def get_days(self, dates: list[str]) -> list | None:
        url = join(self.HOST_BASE_URL, TempoAPI.DAYS) + "?"
        for date in dates:
            if match(TempoAPI.DATE_REGEX, date):
                url += f"{self.API_DAY_DATE}[]={date}&"
            else:
                get_logger().error(
                    f"date must be in YYYY-MM-DD format, currently date was : {date}"
                )
                return None

        url = url[:-1]  # remove leading &
        req = rget(url)

        if req.status_code == 200:
            return self.translate(req.json())

        get_logger().error(f"Can't retrieve {url}")
        return None

    def translate(self, data: any):
        if isinstance(data, list):
            list_translated = []
            for day in data:
                list_translated.append(
                    {
                        "date": day.get(self.API_DAY_DATE),
                        "color_code": day.get(self.API_DAY_COLOR_CODE),
                        "period": day.get(self.API_DAY_PERIOD),
                    }
                )
            return list_translated
        else:
            return {
                "date": data.get(self.API_DAY_DATE),
                "color_code": data.get(self.API_DAY_COLOR_CODE),
                "period": data.get(self.API_DAY_PERIOD),
            }
