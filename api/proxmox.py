#!/usr/bin/env python3

from os import getenv
from os.path import join
from requests import get as rget


class ProxmoxAPI:

    HOST = f"https://{getenv('API_HOST_PROXMOX','pve.local')}"
    API_TOKEN = getenv("API_TOKEN_PROXMOX", None)

    def power_off() -> bool:
        pass

    # curl -k -X POST -H 'Authorization: PVEAPIToken=<ApiToken>=<TokenSecret>' https://<PveIP>:8006/api2/json/nodes/<NodeName>/status/shutdown
