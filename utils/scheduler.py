#!/usr/bin/env python3

import schedule


def register_schedules():

    # Retrieve day color at 11:05 am
    schedule.every().day.at("11:05").do(retrieve_tomorrow_color)

    # Retrieve day color at 12:05 am
    schedule.every().day.at("12:05").do(retrieve_tomorrow_color)

    # Retrieve day color at 20:05 am -> this one is used only if both precedent execution didn't work
    schedule.every().day.at("20:05").do(retrieve_tomorrow_color)

    # Manage server or server (start or stop)
    schedule.every().day.at("21:59").do(server_life_cycle)


def retrieve_tomorrow_color():
    pass


def server_life_cycle():
    pass
