#!/usr/bin/env python3

from os import getenv
from os.path import join
from requests import get as rget


class TastomaAPI:

    HOST = f"http://{getenv('HOST_TASMOTA','tasmota-plug.local')}"

    def get_power_total() -> float:
        command = "EnergyTotal"
        url = join(TastomaAPI.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            return req.json().get("EnergyTotal").get("Total")
        else:
            print(f"Error when retrieve {url}")
            print(req.reason)

    def get_power_yesterday() -> float:
        command = "EnergyYesterday"
        url = join(TastomaAPI.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            return req.json().get("EnergyYesterday").get("Yesterday")
        else:
            print(f"Error when retrieve {url}")
            print(req.reason)

    def get_power_today() -> float:
        command = "EnergyToday"
        url = join(TastomaAPI.HOST, f"cm?cmnd={command}")
        req = rget(url)

        if req.status_code == 200:
            return req.json().get("EnergyToday").get("Today")
        else:
            print(f"Error when retrieve {url}")
            print(req.reason)


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
