# How to start ?

1. Install python3 and python3-venv - can be done with `sudo apt install python3 python3-venv` command on linux
2. Clone repository and open terminal into
3. Run `python3 -m venv .venv`
4. Run `.venv/bin/pip3 install -r requirements.txt`
5. Ready to start ;) 


## The user is not dumb

Explain to the user that days work 22h to 22h. The risk is the need to support user utilisation to answer their questions. They could not understand the system and complexify the user experience.

## We are not rich but

Days start at 22h with the offpeak period, where power price is 0.1568 €/kWh. We could just works with standard days. The will increase the global price of 0.1568 * 22 * 2 * 80 / 1000 = 0,551936 € that is really low price to fix the problem.

# NORMAL CASE

## STARTUP

1. create all day from **env START_SERVER_DATE**
2. fill all these days except current day with the **tasmota TOTAL_POWER**
3. register schedulers
    - every day at 11h05 12h05 20h05 to retrieve next daycolor
    - every day at 6h00 to retrieve consumption of last offpeak
    - every day at 22h00 to retreive consumption of last fullpeak
    - 1st January of each year to compute power debt of each user
    - server life cycle

## DISCORD

1. start bot system and works with several server grouped
    => ask @Mijux for information
2. listen for next commands:
    - `/hello @mention <arrival_date>`
        - `desc`: Add a user to the server project
        - `admin-only`
        - `@mention` **REQUIRED**: discord user name **present** on the server
        - `arrival_date` **OPTIONAL**: must be before or equal the current day and in **YYYY-MM-DD** format
    - `/bye yes`
        - `desc`: User that use this command leave the server
        - `yes` **REQUIRED**: force user to confirm to avoid error when using the command
    - `/bye `@mention``
        - `desc`: Kick the user specified from the server project
        - `admin-only`
        - `user_id` **REQUIRED** discord id user **present** on the server
    - `/set_derogation`
        - `desc`: set a derogation for the current user for next day. Can't be executed after 6h00
    - `/unset_derogation`
        - `desc`: unset a derogation for the current user for next day.
    - `/power_on`
        - `desc`: on the red day, power on the server and automatically add derogation for the user
    - `/get_my_state [all|global|year|month|week|yesterday|today]+ `
        - `desc`: Return consumption and power price for temporalities chosen
    - `/get_state <user_id> [all|global|year|month|week|yesterday|today]+`
        - `desc`: Return consumption and power price for temporalities chosen for the user specified
    - `/get_derogation_state <user_id> [all|global|year|month|week|yesterday|today]+`
        - `desc`: Return consumption and power price for temporalities chosen for the user specified only for derogation
        - `arrival_date` **OPTIONAL**: if no user_id is specified, return the state for author of the message
    - `/op @mention`
        - `desc`: Add a user as admin
        - `admin-only`
        - `@mention` **REQUIRED**: discord user name **present** on the server
    - `/deop @mention`
        - `desc`: Set user as default role
        - `admin-only`
        - `@mention` **REQUIRED**: discord user name **present** on the server
    

## LIFE CYCLE

- If next day is red
    - If has derogation
        - At 6h00 => poweroff server
- else
    - At 22h => poweron the server


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
    -   *at 6h00 => poweroff server ?*
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