#!/usr/bin/env python3

from typing import List
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from uuid import uuid4

from models.base import Base
from models.day import Day

class Pricing(Base):
    __tablename__ = "pricing"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    color: Mapped[int] = mapped_column(Integer, nullable=False)
    hc: Mapped[float] = mapped_column(Float, nullable=False)
    hp: Mapped[float] = mapped_column(Float, nullable=False)

    days: Mapped[List["Day"]] = relationship()

    def __repr__(self) -> str:
        return f"Pricing(id={self.id},color={self.color},hc={self.hc},hp={self.hp})"
