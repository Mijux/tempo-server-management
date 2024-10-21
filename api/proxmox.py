#!/usr/bin/env python3

from os import getenv
from os.path import join
from requests import post as rpost
from wakeonlan import send_magic_packet

from utils.logger import get_logger


class ProxmoxAPI:

    HOST = f"https://{getenv('HOST_PROXMOX','pve.local')}:8006"
    HOST_MAC_ADDR = getenv("HOST_PROXMOX_MAC_ADDR", None)
    TOKEN_ID = getenv("API_PROXMOX_TOKEN_ID", None)
    TOKEN_SECRET = getenv("API_PROXMOX_TOKEN_SECRET", None)

    def power_off() -> bool:

        command = "command=shutdown"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"PVEAPIToken={ProxmoxAPI.TOKEN_ID}={ProxmoxAPI.TOKEN_SECRET}",
        }

        endpoint = "api2/json/nodes/rattler/status"
        url = join(ProxmoxAPI.HOST, endpoint)

        verify_ssl = False
        if getenv("HOST_PROXMOX_SSL_VERIFY", None) in ["true", "y", "1", "yes"]:
            verify_ssl = True

        req = rget(url, verify=verify_ssl, headers=headers, data=command)

        if req.status_code == 200:
            get_logger().info("The server has been shutdown !")
            return True
        else:
            get_logger().error("The server hasn't been shutdown")
            get_logger().debug(req.reason)
            return False

    def power_on() -> bool:
        get_logger().info("Try to wake up server and wait")
        send_magic_packet(ProxmoxAPI.HOST_MAC_ADDR)
