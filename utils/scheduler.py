#!/usr/bin/env python3

import schedule

from datetime import date, timedelta

from api.proxmox import ProxmoxAPI
from api.tempo_day import TempoAPI
from models.day import Day
from utils.db.day import add_day
from utils.dbconn import get_session
from utils.logger import get_logger


def register_schedules():

    # Retrieve day color at 11:05 am
    get_logger().debug(
        "Registering scheduler\n\tfunc: retrieve_next_day_color\n\ttime: every day at 11:05 am"
    )
    schedule.every().day.at("11:05").do(retrieve_next_day_color, "11:05")

    # Retrieve day color at 12:05 am
    get_logger().debug(
        "Registering scheduler\n\tfunc: retrieve_next_day_color\n\ttime: every day at 12:05 am"
    )
    schedule.every().day.at("12:05").do(retrieve_next_day_color, "12:05")

    # Retrieve day color at 20:05 am -> this one is used only if both precedent execution didn't work
    get_logger().debug(
        "Registering scheduler\n\tfunc: retrieve_next_day_color\n\ttime: every day at 20:05 am"
    )
    schedule.every().day.at("20:05").do(retrieve_next_day_color, "20:05")

    # Manage server or server (start or stop)
    get_logger().debug(
        "Registering scheduler\n\tfunc: server_life_cycle_management\n\ttime: every day at 21:55 am"
    )
    schedule.every().day.at("21:55").do(server_life_cycle_management)


def retrieve_next_day_color(exec_hour):
    next_day: date = date.today() + timedelta(days=1)
    day_data = TempoAPI().get_day(next_day.strftime("%Y-%m-%d"))

    if day_data.get("codeJour") == 0:
        get_logger().warning(
            f"The next day ({day_data.get('dateJour')}) color is unknown"
        )
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
    next_day_str: str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    if is_red_day(next_day_str):
        if not has_derogation(next_day_str):
            get_logger().info(
                "Next day is red and no derogation has been emitted : shutdown server"
            )
            ProxmoxAPI().power_off()
        else:
            get_logger().info(
                f"Next day is red but has derogation emitted from {get_derogation_user()} : power on server"
            )
    else:
        get_logger().info("Next day is not red: power on server")

    ProxmoxAPI().power_on()
