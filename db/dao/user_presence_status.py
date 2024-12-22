#!/usr/bin/env python3

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.models.user import User
from db.models.user_presence_status import UserPresenceStatus
from utils.dbconn import get_session

from utils.exceptions import DBUserAlreadyExistsError, DBUserDoesNotExistError, DBUserPresenceOngoingdError


class UserPresenceStatusDao:

    @staticmethod
    def add_user_presence(id: str, username: str, date: str) -> dict:
        with get_session() as db_session:
            if db_session.query(UserPresenceStatus).filter(UserPresenceStatus.id_user==id, UserPresenceStatus.leave_date==None).first() != None:          
                raise DBUserPresenceOngoingdError(id, username)

            try:
                user_presence: UserPresenceStatus = UserPresenceStatus(
                    id_user=id, 
                    arrival_date=date,
                )
                db_session.add(user_presence)
                
                try:
                    db_session.commit()
                except IntegrityError:
                    db_session.rollback()
            except NoResultFound:
                return None
        return True