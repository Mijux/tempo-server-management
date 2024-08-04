#!/usr/bin/env python3

from utils.dbconn import init_db
from utils.db.pricing import init_table

init_db()

init_table()


from api.tempo_day import TempoAPI

print(TempoAPI.get_day("2024-08-04"))
