#!/usr/bin/env python3

from os import getenv
from os.path import join
from platform import system as get_system_name
from requests import post as rpost
from subprocess import call as subcall
from time import sleep
from wakeonlan import send_magic_packet

from utils.logger import get_logger


class ProxmoxStubAPI:

    def __init__(self, poweroff_status=True, poweron_status=True):
        self.poweroff_status = poweroff_status
        self.poweron_status = poweron_status

    def power_off(self) -> bool:
        return self.poweroff_status

    def power_on(self) -> bool:
        return self.poweron_status


class ProxmoxAPI:

    HOST = None
    HOST_BASE_URL = None
    HOST_MAC_ADDR = None
    TOKEN_ID = None
    TOKEN_SECRET = None

    def __init__(self):
        correct = True
        self.HOST = getenv("HOST_PROXMOX", None)
        if not self.HOST:
            correct = False
            get_logger().error(
                "Please assign a value to HOST_PROXMOX variable in your .env file"
            )

        self.HOST_BASE_URL = f"https://{self.HOST}:8006"

        self.HOST_MAC_ADDR = getenv("HOST_PROXMOX_MAC_ADDR", None)
        if not self.HOST_MAC_ADDR:
            correct = False
            get_logger().error(
                "Please assign a value to HOST_PROXMOX_MAC_ADDR in your .env file"
            )

        self.HOST_BOOT_TIMEOUT = getenv("HOST_PROXMOX_BOOT_TIMEOUT", None)
        if not self.HOST_BOOT_TIMEOUT:
            correct = False
            get_logger().error(
                "Please assign a value to HOST_PROXMOX_BOOT_TIMEOUT in your .env file"
            )
        else:
            try:
                self.HOST_BOOT_TIMEOUT = int(self.HOST_BOOT_TIMEOUT)
            except:
                correct = False
                get_logger().error(
                    "Please assign a integer value to HOST_PROXMOX_BOOT_TIMEOUT in your .env file"
                )

        host_proxmox_ssl_verify = getenv("HOST_PROXMOX_SSL_VERIFY", None)
        if not host_proxmox_ssl_verify:
            correct = False
            get_logger().error(
                "Please assign a value to HOST_PROXMOX_SSL_VERIFY in your .env file"
            )
        else:
            self.HOST_SSL_VERIFY = False
            if host_proxmox_ssl_verify in ["true", "y", "1", "yes"]:
                self.HOST_SSL_VERIFY = True

        self.TOKEN_ID = getenv("API_PROXMOX_TOKEN_ID", None)
        if not self.TOKEN_ID:
            correct = False
            get_logger().error(
                "Please assign a value to API_PROXMOX_TOKEN_ID in your .env file"
            )

        self.TOKEN_SECRET = getenv("API_PROXMOX_TOKEN_SECRET", None)
        if not self.TOKEN_SECRET:
            correct = False
            get_logger().error(
                "Please assign a value to API_PROXMOX_TOKEN_SECRET in your .env file"
            )

        if not correct:
            exit(1)

    def power_off(self) -> bool:
        endpoint = "api2/json/nodes/rattler/status"
        command = "command=shutdown"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"PVEAPIToken={self.TOKEN_ID}={self.TOKEN_SECRET}",
        }

        url = join(self.HOST_BASE_URL, endpoint)

        req = rget(url, verify=self.HOST_SSL_VERIFY, headers=headers, data=command)

        if req.status_code == 200:
            get_logger().info("The server has been shutdown !")
            return True
        else:
            get_logger().error("The server hasn't been shutdown")
            get_logger().debug(req.reason)
            return False

    def power_on(self) -> bool:
        get_logger().info("Try to wake up server and wait")
        send_magic_packet(self.HOST_MAC_ADDR)
        sleep(self.HOST_BOOT_TIMEOUT)

        # Windows takes -n as argument and Linux takes -c
        param = "-n" if get_system_name().lower() == "windows" else "-c"

        command = ["ping", param, "1", self.HOST]

        if subcall(command) == 0:
            get_logger().info("Server has been power on successfully")
            return True

        get_logger().error(
            "Can't check if server is powered on - pls check your WOL config or increase timeout"
        )
        return False
