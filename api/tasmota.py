#!/usr/bin/env python3

from os import getenv
from os.path import join
from requests import get as rget

from utils.logger import get_logger


class TastomaAPI:

    HOST = f"http://{getenv('HOST_TASMOTA','tasmota-plug.local')}"

    def get_power_total() -> float:
        command = "EnergyTotal"
        url = join(TastomaAPI.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            total_power = req.json().get("EnergyTotal").get("Total")
            get_logger().info(f"EnergyTotal has been retrieved : {total_power}")
            return total_power
        else:
            get_logger().error(f"Cannot retrieve {url}")
            get_logger().debug(req.reason)

    def get_power_yesterday() -> float:
        command = "EnergyYesterday"
        url = join(TastomaAPI.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            yesterday_power = req.json().get("EnergyYesterday").get("Total")
            get_logger().info(f"EnergyYesterday has been retrieved : {yesterday_power}")
            return yesterday_power
        else:
            get_logger().error(f"Cannot retrieve {url}")
            get_logger().debug(req.reason)

    def get_power_today() -> float:
        command = "EnergyToday"
        url = join(TastomaAPI.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            today_power = req.json().get("EnergyToday").get("Total")
            get_logger().info(f"EnergyToday has been retrieved : {today_power}")
            return today_power
        else:
            get_logger().error(f"Cannot retrieve {url}")
            get_logger().debug(req.reason)


"""     def power_on() -> bool:
        command = "Power%20on"
        url = join(TastomaAPI.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            return True
        else:
            print(f"Error when retrieve {url}")
            print(req.reason)
            return False

    def power_off() -> bool:
        command = "Power%20off"
        url = join(TastomaAPI.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            return True
        else:
            print(f"Error when retrieve {url}")
            print(req.reason)
            return False """
