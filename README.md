# How to start ?

1. Install python3 and python3-venv - can be done with `sudo apt install python3 python3-venv` command on linux
2. Clone repository and open terminal into
3. Run `python3 -m venv .venv`
4. Run `.venv/bin/pip3 install -r requirements.txt`
5. Ready to start ;) 


# NORMAL CASE

## STARTUP

1. create all day from **env START_SERVER_DATE**
2. fill all these days except current day with the **tasmota TOTAL_POWER**
3. register schedulers
    - every day at 11h05 12h05 20h05 to retrieve next daycolor
    - every day at 6h00 to retrieve consumption of last offpeak
    - every day at 22h00 to retreive consumption of last fullpeak
    - 1st January of each year to compute power debt of each user

## DISCORD

1. start bot system and works with several server grouped
    => ask @Mijux for information
2. listen for next commands:
    - `/hello_you <user_id> <arrival_date>`
        - `admin-only`
        - `user_id` **REQUIRED** discord id user **present** on the server
        - `arrival_date` **OPTIONAL** must be before or equal the current day and in **YYYY-MM-DD** format
    - `/bye_bye`
    - `/bye_bye <user_id>`
        - `admin-only`
        - `user_id` **REQUIRED** discord id user **present** on the server
    - `/change_date [arrival|leave] <date> <user_id>`
        - `admin-only`
        - `date` **REQUIRED** must be before or equal the current day and in **YYYY-MM-DD** 
        - `user_id` **REQUIRED** discord id user **present** on the server
format
    - `/set_derogation [today/tomorrow] <hour_start> <hour_end>`
        - `hour_start` not mandatory. By default if "today" is select, the derogation will be avalaible as soon as possible. If tomorrow is choosen by the user, the hour start is 6am.
        - `hour_end` not mandatory. By default the derogation last 12 hours.
        - return a **derogation id**
    - `/remove_derogation` <derogation_id>
        - can't be executed after 21h45
        - `derogation_id` **required**
    - `/get_my_current_derogations`
        - return derogation_id and description derogation ( start hour and end hour )        
    - `/get_total_state` [all/global/year/week/yesterday/day]
        - return global consumption since server start and price (for all and global)
        - return consumption from last year and price (for all and year)
        - return consumption from one week and price (for all and week)
        - return consumption from yesterday and price (for all and yesterday)
        - return current consumption of the day and price (for all and day)
    - `/get_my_state` [all/global/year/week/yesterday/day/derogations_year/derogations_total]
        - return global consumption since server start and price (for all and global)
        - return consumption from last year and price (for all and year)
        - return consumption from one week and price (for all and week)
        - return consumption from yesterday and price (for all and yesterday)
        - return current consumption of the day and price (for all and day)
        - return current consumption of the derogation of the current and price (for all and derogations_year)
        - return current consumption of the derogation since arrival date and price (for all and derogations_total)

## LIFE CYCLE

- If next day is red
    - If has derogation
        - At 22h00 => poweroff server
- else
    - At 6h => poweron the server


# PROBLEM CASE 1

This case appear when internet is down.

## WHEN INTERNET IS UP

1. create day that are missing
2. fill these days except the current day with the result of
    - **tasmota TOTAL_POWER** - **db TOTAL_POWER**
3. register schedulers
    - handle case where days are missing
        - if day are missing launch a restore as startup functions do 

## LIFE CYCLE

-   if next day is unknow (because of internet)
    -   *at 22h00 => poweroff server ?*
        > What must be the default behavior ? 

# PROBLEM CASE 2

This case appear when the tasmota plug is broken.

## STARTUP TSM WHEN A NEW PLUG IS PLUGGED

1. create days that are missing
2. register schedulers
    - if **db LAST_STATE** > **tasmota TOTAL_POWER**
        - then dont fill missing days (put them at -1 to say down)

## LIFE CYCLE

-   Nothing, the server is down because out of power
    - Just we need to ensure that the server can powerdown safely thanks to inverter

# PROBLEM CASE 3

The TSM code is down

## STARTUP TSM

1. create days that are missing
2. register schedulers
    - if **db LAST_STATE** < **tasmota TOTAL_POWER**
        - then fill missing days with the average power day
