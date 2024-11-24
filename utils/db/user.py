#!/usr/bin/env python3

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.user import User
from utils.dbconn import get_session

from utils.exceptions import DBUserAlreadyExistsError, DBUserDoesNotExistError


def add_user(user: dict) -> bool:
    with get_session() as db_session:
        new_user: User = User(
            id=user.get("id"),
            username=user.get("username"),
            avatar=user.get("avatar"),
            permission_level=0,
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
        user_to_remove: User | None = (
            db_session.query(User).filter(User.id == user_id).first()
        )

        leave_date = datetime.now().strftime("%Y-%m-%d")

        try:
            user_to_remove.leave_date = leave_date
            db_session.commit()
        except:
            raise DBUserDoesNotExistError(user_id)

    return True
