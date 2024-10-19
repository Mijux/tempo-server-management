#!/usr/bin/env python3

from api.tempo_day import TempoAPI

from utils.dbconn import init_db
from utils.db.pricing import init_pricing_table
from utils.db.day import init_day_table
from utils.scheduler import register_schedules

init_db()
init_pricing_table()
init_day_table()

register_schedules()
