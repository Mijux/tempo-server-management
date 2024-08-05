#!/usr/bin/env python3

from api.tempo_day import TempoAPI

from utils.dbconn import init_db
from utils.db.pricing import init_table
from utils.scheduler import retrieve_next_day_color

init_db()
init_table()


retrieve_next_day_color("11:05")
