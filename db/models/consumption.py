#!/usr/bin/env python3

from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class Consumption(Base):
    __tablename__ = "consumption"

    date: Mapped[str] = mapped_column(ForeignKey("day.date"), primary_key=True)
    begin_hour: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_hour: Mapped[int] = mapped_column(Integer, primary_key=True)
    begin_consumption_power: Mapped[float] = mapped_column(Float)
    end_consumption_power: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return f"Derogation(id_user={self.id_user},date={self.date},begin_hour={self.begin_hour},end_hour={self.end_hour},begin_consumption_power={self.begin_consumption_power},end_consumption_power={self.end_consumption_power})"
