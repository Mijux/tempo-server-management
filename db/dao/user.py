#!/usr/bin/env python3

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.models.user import User
from db.models.user_presence_status import UserPresenceStatus
from utils.dbconn import get_session

from utils.exceptions import DBError, DBUserAlreadyExistsError, DBUserDoesNotExistError, DBUserNotPresent


def get_user(id: str) -> User | None:
    with get_session() as db_session:
        try:
            return db_session.query(User).filter(User.id==id).first()
        except NoResultFound:
            return None
    return True

def update_user(user_updated: dict) -> dict:
    with get_session() as db_session:
            
        try:
            user = db_session.query(User).filter(User.id==id)
        except NoResultFound:
            raise DBUserDoesNotExistError(user_updated.get("id"))
        if user:
            user.avatar = user_updated.get("avatar")
            user.username = user_updated.get("username")

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            return DBError

    return True

def add_user(user: dict) -> bool:
    with get_session() as db_session:
        new_user: User = User(
            id=user.get("id"),
            username=user.get("username"),
            avatar=user.get("avatar"),
            permission_level=1,
        )

        db_session.add(new_user)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise DBUserAlreadyExistsError(user.get("id"), user.get("username"))

    return True

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

def remove_user(user_id: str) -> bool:
    with get_session() as db_session:
        db_session.query(User).filter(User.id==user_id).delete()

        try:
            db_session.commit()
        except:
            raise DBUserDoesNotExistError(user_id)

    return True
