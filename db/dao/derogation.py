#!/usr/bin/env python3

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.models.user import User
from db.models.day import Day
from db.models.derogation import Derogation
from utils.dbconn import get_session

from utils.exceptions import (
    DBUserAlreadyExistsError,
    DBDayDoesNotExistError,
    DBUserDoesNotExistError,
    DBDerogationAlreadyExistsError,
    DBDerogationDoesNotExistError,
)


def add_derogation(user_id: str, date: str) -> bool:
    with get_session() as db_session:
        user: User | None = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            raise DBUserDoesNotExistError(user_id)

        day: User | None = db_session.query(Day).filter(Day.date == date).first()
        if not day:
            raise DBDayDoesNotExistError(date)

        new_derogation: Derogation = Derogation(id_user=user_id, date=date)
        db_session.add(new_derogation)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise DBDerogationAlreadyExistsError(user_id, date)

    return True


def delete_derogation(user_id: str, date: str) -> bool:
    with get_session() as db_session:
        derogation_to_del: Derogation | None = (
            db_session.query(Derogation)
            .filter(Derogation.id_user == user_id, Derogation.date == date)
            .first()
        )

        db_session.delete(derogation_to_del)
        try:
            db_session.commit()
        except:
            db_session.rollback()
            raise DBDerogationDoesNotExistError(user_id, date)

    return True


def get_derogations() -> list[Derogation]:
    with get_session() as db_session:

        derogation: Derogation | None = db_session.query(Derogation).all()

        return derogation


def get_derogation(user_id: str, date: str) -> Derogation:
    with get_session() as db_session:

        derogation: Derogation | None = (
            db_session.query(Derogation)
            .filter(Derogation.id_user == user_id, Derogation.date == date)
            .first()
        )

        if not derogation:
            raise DBDerogationDoesNotExistError(user_id, date)

        return derogation


def get_derogation_per_date(date: str) -> list[Derogation] | None:
    with get_session() as db_session:

        derogations: Derogation | None = (
            db_session.query(Derogation).filter(Derogation.date == date).all()
        )

        if not derogations or len(derogations) == 0:
            raise DBDerogationDoesNotExistError(date=date)

        return derogations


def get_derogation_per_user(
    user_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[Derogation] | None:
    with get_session() as db_session:

        q = db_session.query(Derogation).filter(Derogation.id_user == user_id)

        if start_date:
            q = q.filter(Derogation.date >= start_date)

        if end_date:
            q = q.filter(Derogation.date <= end_date)

        derogations: list[Derogation] = q.all()

        if not derogations or len(derogations) == 0:
            raise DBDerogationDoesNotExistError(user_id=user_id)

        return derogations


def get_derogation_users(date: str) -> list[str] | None:
    with get_session() as db_session:
        derogations: list[Derogation] = (
            db_session.query(Derogation).filter(Derogation.date == date).all()
        )

        users = []
        for derogation in derogations:
            users.append(derogation.id_user)

        return users
