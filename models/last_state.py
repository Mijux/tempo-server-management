#!/usr/bin/env python3

from datetime import datetime
from pytz import timezone
from typing import List
from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from os import getenv
from uuid import uuid4

from models.base import Base
from models.derogation import Derogation


def current_hour() -> str:
    return datetime.now().strftime("%H")


class LastState(Base):
    __tablename__ = "lastState"

    date: Mapped[str] = mapped_column(ForeignKey("day.date"), primary_key=True)
    time: Mapped[str] = mapped_column(String, primary_key=True, default=current_hour)
    consumption: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"User(date={self.date},time={self.time},consumption={self.consumption})"
