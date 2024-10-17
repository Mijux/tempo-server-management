#!/usr/bin/env python3

import schedule

from datetime import date, timedelta

from api.tempo_day import TempoAPI
from models.day import Day
from utils.db.day import add_day
from utils.dbconn import get_session


def register_schedules():

    # Retrieve day color at 11:05 am
    schedule.every().day.at("11:05").do(retrieve_next_day_color, "11:05")

    # Retrieve day color at 12:05 am
    schedule.every().day.at("12:05").do(retrieve_next_day_color, "12:05")

    # Retrieve day color at 20:05 am -> this one is used only if both precedent execution didn't work
    schedule.every().day.at("20:05").do(retrieve_next_day_color, "20:05")

    # Manage server or server (start or stop)
    schedule.every().day.at("21:55").do(server_life_cycle_management)


def retrieve_next_day_color(exec_hour):
    next_day: date = date.today() + timedelta(days=1)
    day_data = TempoAPI.get_day(next_day.strftime("%Y-%m-%d"))

    if day_data.get("codeJour") == 0:
        print(f"> Le code du jour suivant {day_data.get('dateJour')} est inconnu")
    else:
        with get_session() as db_session:

            has_day = (
                db_session.query(Day)
                .filter(Day.date == day_data.get("dateJour"))
                .first()
            )

            if not has_day():
                add_day(db_session, day_data)
            db_session.commit()


def server_life_cycle_management():
    # TODO retrieve next day from the database
    next_day = None

    if next_day and next_day.color == red:
        if not derogation:
            stop_serveur()
            return

    startup_serveur()

    pass
