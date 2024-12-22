#!/usr/bin/env python3

from typing import List
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from uuid import uuid4

from db.models.base import Base
from db.models.day import Day


class Pricing(Base):
    __tablename__ = "pricing"

    period: Mapped[str] = mapped_column(String, primary_key=True)
    color: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[UUID] = mapped_column(UUID, default=uuid4, nullable=False, unique=True)
    price_fullpeak: Mapped[float] = mapped_column(Float, nullable=False)
    price_offpeak: Mapped[float] = mapped_column(Float, nullable=False)

    days: Mapped[List["Day"]] = relationship()

    def __repr__(self) -> str:
        return f"Pricing(period={self.period},color={self.color},id={self.id},price_fullpeak={self.price_fullpeak},price_offpeak={self.price_offpeak},days={self.days})"
