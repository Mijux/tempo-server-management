#!/usr/bin/env python3


class ConfigurationException(Exception):
    pass


class DBError(Exception):
    pass


class DBUserAlreadyExistsError(Exception):
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.err_msg = f"The user {self.username}({self.id}) already exists"

        super().__init__(self.err_msg)

class DBUserPresenceOngoingdError(Exception):
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.err_msg = f"The user {self.username}({self.id}) already has an ongoing presence"

        super().__init__(self.err_msg)


class DBUserDoesNotExistError(Exception):
    def __init__(self, id):
        self.id = id
        self.err_msg = f"The user with id {self.id} does not exist"

        super().__init__(self.err_msg)


class DBPricingInsertionError(Exception):
    def __init__(self, color, period):
        self.color = color
        self.period = period
        self.err_msg = f"The following pricing {period}:{color} already exists or the database is corrupted"

        super().__init__(self.err_msg)


class DBPricingDoesNotExistError(Exception):
    def __init__(self, color, period):
        self.color = color
        self.period = period
        self.err_msg = f"The following pricing {period}:{color} does not exist"

        super().__init__(self.err_msg)


class DBDayAlreadyExistsError(Exception):
    def __init__(self, date):
        self.date = date
        self.err_msg = f"The day {date} already exists"

        super().__init__(self.err_msg)


class DBDayDoesNotExistError(Exception):
    def __init__(self, date):
        self.date = date
        self.err_msg = f"The day {date} does not exist"

        super().__init__(self.err_msg)


class DBDerogationAlreadyExistsError(Exception):
    def __init__(self, user_id, date):
        self.id = user_id
        self.date = date
        self.err_msg = f"The derogation for {self.id} on {self.date} already exists"

        super().__init__(self.err_msg)


class DBDerogationDoesNotExistError(Exception):
    def __init__(self, user_id="unknown", date="unknown"):
        self.id = user_id
        self.date = date
        self.err_msg = f"The derogation for {self.id} on {self.date} does not exist"

        super().__init__(self.err_msg)
