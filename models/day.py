#!/usr/bin/env python3

from typing import List
from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from uuid import uuid4

from models.base import Base
from models.derogation import Derogation


class Day(Base):
    __tablename__ = "day"

    date: Mapped[str] = mapped_column(String, primary_key=True)
    id_pricing: Mapped[UUID] = mapped_column(ForeignKey("pricing.id"), nullable=False)
    consumption_offpeak: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    consumption_fullpeak: Mapped[float] = mapped_column(
        Float, nullable=False, default=0
    )

    derogations: Mapped[List["Derogation"]] = relationship()

    def __repr__(self) -> str:
        return f"Day(date={self.date},id_pricing={self.id_pricing},consumption_offpeak={self.consumption_offpeak},consumption_fullpeak={self.consumption_fullpeak})"
