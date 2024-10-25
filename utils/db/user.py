#!/usr/bin/env python3

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
            arrival_date=user.get("arrival_date"),
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
        user_to_remove: User = db_session.query(User).filter(User.id == user_id).first()

        if user_to_remove:
            db_session.delete(user_to_remove)
            db_session.commit()
        else:
            raise DBUserDoesNotExistError(user_id)

    return True
