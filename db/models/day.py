#!/usr/bin/env python3

from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID

from db.models.base import Base
from db.models.derogation import Derogation
from db.models.consumption import Consumption


class Day(Base):
    __tablename__ = "day"

    date: Mapped[str] = mapped_column(String, primary_key=True)
    id_pricing: Mapped[UUID] = mapped_column(ForeignKey("pricing.id"), nullable=False)

    derogations: Mapped[List["Derogation"]] = relationship()
    consumption: Mapped[List["Consumption"]] = relationship()

    def __repr__(self) -> str:
        return f"Day(date={self.date},id_pricing={self.id_pricing},consumption_offpeak={self.consumption},consumption_fullpeak={self.derogations})"
