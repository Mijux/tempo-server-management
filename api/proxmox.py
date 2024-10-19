#!/usr/bin/env python3

from os import getenv
from os.path import join
from requests import post as rpost
from wakeonlan import send_magic_packet


class ProxmoxAPI:

    HOST = f"https://{getenv('HOST_PROXMOX','pve.local')}"
    HOST_MAC_ADDR = getenv("HOST_PROXMOX_MAC_ADDR", None)
    TOKEN_ID = getenv("API_PROXMOX_TOKEN_ID", None)
    TOKEN_SECRET = getenv("API_PROXMOX_TOKEN_SECRET", None)

    def power_off() -> bool:

        command = "command=shutdown"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"{ProxmoxAPI.TOKEN_ID}={ProxmoxAPI.TOKEN_SECRET}",
        }

        endpoint = "/api2/json/nodes/rattler/status"
        url = join(ProxmoxAPI.HOST, endpoint)

        req = rget(url, headers=headers, data=command, verify=False)

        if req.status_code == 200:
            return True
        else:
            print(f"Error when retrieve {url}")
            print(req.reason)
            return False

    def power_on() -> bool:
        send_magic_packet(ProxmoxAPI.HOST_MAC_ADDR)
