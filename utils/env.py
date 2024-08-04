#!/usr/bin/env python3

from flask import current_app as app
from os import environ


def check_dotenv() -> bool:
    """
    This function check if necessary dotenv parameters are setup and add it to flask config dict.
    This allow to use flask context to retrieve parameters

    return: True if necessary parameters are present else False
    """
    ret = True


    """
    ################# Example #################

    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY") or None
    if not JWT_SECRET_KEY:
        print("Missing JWT_SECRET_KEY")
        ret = False
    else:
        app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    ###########################################
    """

    return ret