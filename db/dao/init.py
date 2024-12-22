#!/usr/bin/env python3

from db.models.base import Base
from utils.dbconn import EngineSingleton
from db.dao.pricing import init_pricing_table
from db.dao.day import init_day_table
from db.dao.consumption import init_consumption_table


def init_db():
    Base.metadata.create_all(EngineSingleton().get_engine())


def init():
    init_db()
    init_pricing_table()
    init_day_table()
    init_consumption_table()
