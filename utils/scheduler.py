#!/usr/bin/env python3

from pytz import timezone
import schedule

from datetime import datetime, date, timedelta
from os import getenv
from time import sleep
from threading import Thread, Event as TEvent

from api.proxmox import ProxmoxAPI, ProxmoxStubAPI
from api.tasmota import TastomaAPI
from api.tempo_day import TempoAPI
from models.consumption import Consumption
from models.day import Day
from utils.db.day import add_day, has_derogation, is_red_day
from utils.db.consumption import add_consumption
from utils.db.derogation import get_derogation_users
from utils.dbconn import get_session
from utils.logger import get_logger


def get_schedule_jobs() -> list[schedule.Job] | None:
    return schedule.get_jobs()


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = TEvent()

    class ScheduleThread(Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def register_schedules():

    # Retrieve day color at 11:05 am
    get_logger().debug(
        "Registering scheduler\n\tfunc: retrieve_next_day_color\n\ttime: every day at 11:05 am"
    )
    schedule.every().day.at("11:05").do(retrieve_next_day_color, "11:05")

    # Retrieve day color at 12:05 pm
    get_logger().debug(
        "Registering scheduler\n\tfunc: retrieve_next_day_color\n\ttime: every day at 12:05 pm"
    )
    schedule.every().day.at("12:05").do(retrieve_next_day_color, "12:05")

    # Retrieve day color at 8:05 pm -> this one is used only if both precedent execution didn't work
    get_logger().debug(
        "Registering scheduler\n\tfunc: retrieve_next_day_color\n\ttime: every day at 8:05 am"
    )
    schedule.every().day.at("20:05").do(retrieve_next_day_color, "20:05")

    get_logger().debug(
        "Registering scheduler\n\tfunc: retrieve_hourly_consumption\n\ttime: every hours at :00"
    )
    schedule.every().hour.at(":00").do(retrieve_hourly_consumption)

    # Manage server or server (start or stop)
    get_logger().debug(
        "Registering scheduler\n\tfunc: server_life_cycle_management\n\ttime: every day at 5:55 am"
    )
    schedule.every().day.at("05:55").do(server_life_cycle_management)


def retrieve_hourly_consumption():
    tz = timezone(getenv("TIMEZONE"))
    current_time = datetime.now().replace(minute=0, tzinfo=tz)
    current_date = datetime.today().replace(hour=current_time.hour, minute=0, tzinfo=tz)
    if current_time.hour < 6:
        current_date += timedelta(days=-1)

    with get_session() as db_session:
        previous_consumption = (
            db_session.query(Consumption).order_by(Consumption.end_hour.desc()).first()
        )

        consumption_from_plug = TastomaAPI().get_power_total()

        add_consumption(
            current_date.strftime("%Y-%m-%d"),
            previous_consumption.end_hour,
            current_time.timestamp(),
            previous_consumption.end_consumption_power,
            consumption_from_plug,
        )


def retrieve_next_day_color():
    next_day: date = date.today() + timedelta(days=1)
    day_data = TempoAPI().get_day(next_day.strftime("%Y-%m-%d"))

    if day_data.get("color_code") == 0:
        get_logger().warning(f"The next day ({day_data.get('date')}) color is unknown")
    else:
        with get_session() as db_session:

            has_day = (
                db_session.query(Day).filter(Day.date == day_data.get("date")).first()
            )

            if not has_day():
                add_day(day_data)
            db_session.commit()


def server_life_cycle_management():
    next_day_str: str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    if is_red_day(next_day_str):
        if not has_derogation(next_day_str):
            get_logger().info(
                "Next day is red and no derogation has been emitted : shutdown server"
            )

            if getenv("ENVIRONMENT", None).upper() == "PROD":
                ProxmoxAPI().power_off()
            else:
                ProxmoxStubAPI().power_off()
        else:
            users = get_derogation_users(next_day_str)
            get_logger().info(
                f"Next day is red but has derogation emitted from {users} : power on server"
            )
    else:
        get_logger().info("Next day is not red: power on server")

    if getenv("ENVIRONMENT", None).upper() == "PROD":
        ProxmoxAPI().power_on()
    else:
        ProxmoxStubAPI().power_on()
