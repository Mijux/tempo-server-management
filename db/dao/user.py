#!/usr/bin/env python3

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.models.user import User
from db.models.user_presence_status import UserPresenceStatus
from utils.dbconn import get_session

from utils.enums.role import RoleE
from utils.exceptions import DBError, DBUserAlreadyExistsError, DBUserDoesNotExistError, DBUserNotPresent


def get_user(user_id: str, session: Session | None = None) -> User | None:
    if session: 
        return session.query(User).filter(User.id==user_id).first()
    else:
        with get_session() as db_session:
            try:
                return db_session.query(User).filter(User.id==user_id).first()
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


def remove_user(user_id: str) -> bool:
    with get_session() as db_session:
        db_session.query(User).filter(User.id==user_id).delete()

        try:
            db_session.commit()
        except:
            raise DBUserDoesNotExistError(user_id)

    return True



def change_role_user(user_id: str,role_user: RoleE) -> bool:
    with get_session() as db_session:
        user = get_user(user_id, db_session)
        if user != None: 
           user.permission_level = int(role_user.value)
        else: 
            raise DBUserDoesNotExistError(user_id)
        try:
            db_session.commit()
        except IntegrityError as e:
            db_session.rollback()
            raise DBError

    return True