#!/usr/bin/env python3

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.dao.user import get_user
from db.models.user import User
from db.models.user_presence_status import UserPresenceStatus
from utils.dbconn import get_session

from utils.exceptions import DBError, DBUserAlreadyExistsError, DBUserDoesNotExistError, DBUserNotPresent, DBUserPresenceOngoingdError


class UserPresenceStatusDao:

    @staticmethod
    def leave_user(user_id: str) -> bool:
        with get_session() as db_session:
            user = get_user(user_id)
            if user != None: 
                user_presence = db_session.query(UserPresenceStatus).filter(UserPresenceStatus.id_user==user_id,UserPresenceStatus.leave_date == None).first()
                if user_presence == None:
                    raise DBUserNotPresent(user_id)
                else :
                    user_presence.leave_date = datetime.now() + timedelta(days=1)
            else: 
                raise DBUserDoesNotExistError(user_id)
            try:
                db_session.commit()
            except IntegrityError:
                db_session.rollback()
                raise DBError

        return True

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
    