#!/usr/bin/env python3

from datetime import datetime, date, timedelta
from os import getenv

from pytz import timezone
from db.dao.day import get_day, get_days_with_derogations
from db.dao.pricing import get_pricing
from db.models.day import Day
from utils.dbconn import get_session
from utils.enums.period import PeriodE

from db.dao.user import get_user
from db.dao.consumption import get_consumption, get_last_entry_for_year, get_first_entry_for_year
from db.dao.derogation import get_derogations

class Stats:

    @staticmethod
    def get_user_state(user_id: str, period: int, only_derogation=False):
        """
        used for /get_my_state and /get_state <user_id>

        {
            "server": {
                consumption: 100,
                price: 10
            },
            "user": {
                consumption: 30,
                price: 3,
                derogation: {
                    number_of_derog: 2,
                    consumption: 5,
                    price: 2
                }
            }
        }

        """
        period_e = PeriodE.from_number(period)

        if not period_e:
            return None  # Here should be an exception

        if not get_user(user_id):
            return None  # Here should be an exception

        if period_e is PeriodE.GLOBAL:
            return Stats.get_global(user_id,only_derogation)
        elif period_e is PeriodE.YEAR:
            return Stats.get_year()
        elif period_e is PeriodE.MONTH:
            return Stats.get_month()
        elif period_e is PeriodE.WEEK:
            return Stats.get_week()
        elif period_e is PeriodE.YESTERDAY:
            return Stats.get_day(-1)
        elif period_e is PeriodE.TODAY:
            return Stats.get_day(0)
        else:
            pass
    
    @staticmethod
    def get_global(user_id: str, only_derogatiuon: bool):
        ret = {}
        ret["server"]["consumption"]

    @staticmethod
    def get_year(user_id: str, only_derogatiuon: bool):
        pass
    
    @staticmethod
    def get_month(user_id: str, only_derogatiuon: bool):
        pass

    @staticmethod
    def get_week(user_id: str, only_derogatiuon: bool):
        pass
    
    @staticmethod
    def get_day(user_id: str, only_derogatiuon: bool):
        pass

    @staticmethod
    def compute_power_between_date(start_date: str, end_date: str) -> int:
        first_day = get_day(start_date, with_consumption=True)
        first_consumption = sorted(first_day.consumptions, key=lambda x: x.begin_hour)[0]
        
        last_day = get_day(end_date, with_consumption=True)
        last_consumption = sorted(last_day.consumptions, key=lambda x: x.end_hour, reverse=True)[0]
        
        return abs(first_consumption.begin_consumption_power - last_consumption.end_consumption_power)
        
    @staticmethod
    def compute_power_price_day(date : str):
        tz = timezone(getenv("TIMEZONE"))
        day = get_day(date, with_consumption=True)
        pricing = get_pricing(day.id_pricing)
        
        total_price = 0
        
        for consumption in day.consumptions:
            shour = datetime.fromtimestamp(consumption.begin_hour,tz)
            
            kwh_price = None
            if shour.hour >= 6 and shour.hour < 22:
                kwh_price = pricing.price_fullpeak
            else:
                kwh_price = pricing.price_offpeak
                
            total_price += kwh_price * abs(consumption.end_consumption_power * consumption.begin_consumption_power)
            
        return total_price

    @staticmethod
    def compute_derogation_price_day(date: str):
        day_price = Stats.compute_power_price_day(date)
        day = get_day(date, with_derogations=True)
        return day_price / len(day.derogations)
        