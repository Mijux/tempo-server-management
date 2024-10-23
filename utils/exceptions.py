#!/usr/bin/env python3


""" class SignatureException(Exception):
    error_code = 403


class GithubException(Exception):
    error_code = 500


class DeployException(Exception):
    error_code = 500 """


class ConfigurationException(Exception):
    pass


class DBUserAlreadyExistsError(Exception):

    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.err_msg = f"The user {self.username}({self.id}) already exists"

        super().__init__(self.err_msg)


class DBUserDoesNotExistError(Exception):
    def __init__(self, id):
        self.id = id
        self.err_msg = f"The user with id {self.id} does not exist"
