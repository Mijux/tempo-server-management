#!/usr/bin/env python3

from os import getenv
from os.path import join
from platform import system as get_system_name
from requests import post as rpost
from subprocess import call as subcall
from time import sleep
from wakeonlan import send_magic_packet

from utils.logger import get_logger


class ProxmoxAPI:

    HOST = getenv("HOST_PROXMOX", "pve.local")
    HOST_BASE_URL = f"https://{HOST}:8006"
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
        url = join(ProxmoxAPI.HOST_BASE_URL, endpoint)

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
        sleep(60)

        # Windows takes -n as argument and Linux takes -c
        param = "-n" if get_system_name().lower() == "windows" else "-c"

        command = ["ping", param, "1", ProxmoxAPI.HOST]

        if subcall(command) == 0:
            get_logger().info("Server has been power on successfully")
            return True

        get_logger().error(
            "Can't check if server is powered on - pls check your WOL config or increase timeout"
        )
        return False
