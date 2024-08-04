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
    conso_hc: Mapped[float] = mapped_column(Float, nullable=True)
    conso_hp: Mapped[float] = mapped_column(Float, nullable=True)

    derogations: Mapped[List["Derogation"]] = relationship()

    def __repr__(self) -> str:
        return f"Day(date={self.date},id_pricing={self.id_pricing},conso_hc={self.conso_hc},conso_hp={self.conso_hp})"
