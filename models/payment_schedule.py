#!/usr/bin/env python3

from typing import List
from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from uuid import uuid4

from models.base import Base
from models.derogation import Derogation


class PaymentSchedule(Base):
    __tablename__ = "paymentSchedule"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)
    year: Mapped[str] = mapped_column(String, primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id},year={self.year},amount={self.amount},paid={self.paid})"
