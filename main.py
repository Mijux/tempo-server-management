#!/usr/bin/env python3

from dotenv import load_dotenv
from os import getenv

from api.tempo_day import TempoAPI
from api.proxmox import ProxmoxAPI, ProxmoxStubAPI

from utils.db.init import init as db_init
from utils.scheduler import register_schedules, run_continuously, get_schedule_jobs
from utils.logger import setup_logger, get_logger

load_dotenv()
setup_logger()

if not getenv("ENVIRONMENT", None):
    get_logger().error(
        "Please assign a value to ENVIRONMENT variable in your .env file"
    )
    exit(1)

if not getenv("TIMEZONE", None):
    get_logger().error(
        "Please assign a value to ENVIRONMENT variable in your .env file"
    )
    exit(1)


is_test = False

if not is_test:
    db_init()
    register_schedules()
else:
    pass

get_logger().info("Start Background Scheduler")
stop_run_continuously = run_continuously()

get_logger().info(f"Jobs executed are {get_schedule_jobs()}")
