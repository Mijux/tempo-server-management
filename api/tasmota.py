#!/usr/bin/env python3

from os import getenv
from os.path import join
from requests import get as rget

from utils.logger import get_logger


class TastomaStubAPI:

    def __init__(self, total=200, today=1, yesterday=1.3):
        self.total = total
        self.today = today
        self.yesterday = yesterday

    def get_power_total(self) -> float:
        return float(self.total)

    def get_power_today(self) -> float:
        return float(self.today)

    def get_power_yesterday(self) -> float:
        return float(self.yesterday)


class TastomaAPI:

    HOST = None
    HOST_BASE_URL = None

    def __init__(self):
        correct = True
        self.HOST = getenv("HOST_TASMOTA", None)
        if not self.HOST:
            correct = False
            get_logger().error(
                "Please assign a value to HOST_TASMOTA variable in your .env file"
            )

        self.HOST_BASE_URL = f"http://{self.HOST}"

        if not correct:
            exit(1)

    def get_power_total(self) -> float:
        command = "EnergyTotal"
        url = join(self.HOST_BASE_URL, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            total_power = req.json().get("EnergyTotal").get("Total")
            get_logger().info(f"EnergyTotal has been retrieved : {total_power}")
            return total_power
        else:
            get_logger().error(f"Cannot retrieve {url}")
            get_logger().debug(req.reason)

    def get_power_yesterday(self) -> float:
        command = "EnergyYesterday"
        url = join(self.HOST_BASE_URL, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            yesterday_power = req.json().get("EnergyYesterday").get("Total")
            get_logger().info(f"EnergyYesterday has been retrieved : {yesterday_power}")
            return yesterday_power
        else:
            get_logger().error(f"Cannot retrieve {url}")
            get_logger().debug(req.reason)

    def get_power_today(self) -> float:
        command = "EnergyToday"
        url = join(self.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            today_power = req.json().get("EnergyToday").get("Total")
            get_logger().info(f"EnergyToday has been retrieved : {today_power}")
            return today_power
        else:
            get_logger().error(f"Cannot retrieve {url}")
            get_logger().debug(req.reason)
