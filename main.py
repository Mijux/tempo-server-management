#!/usr/bin/env python3

from dotenv import load_dotenv

from api.tempo_day import TempoAPI
from api.proxmox import ProxmoxAPI, ProxmoxStubAPI
from utils.dbconn import init_db
from utils.db.pricing import init_pricing_table
from utils.db.day import init_day_table, init_fill_power_consumption
from utils.scheduler import register_schedules

load_dotenv()

is_test = False

if is_test:
    pass
else:
    init_db()
    init_pricing_table()
    init_day_table()
    init_fill_power_consumption()
    register_schedules()
