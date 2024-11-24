#!/usr/bin/env python3

from models.base import Base
from utils.dbconn import EngineSingleton
from utils.db.pricing import init_pricing_table
from utils.db.day import init_day_table
from utils.db.consumption import init_consumption_table


def init_db():
    Base.metadata.create_all(EngineSingleton().get_engine())


def init():
    init_db()
    init_pricing_table()
    init_day_table()
    init_consumption_table()
