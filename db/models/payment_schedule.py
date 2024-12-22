#!/usr/bin/env python3

from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class PaymentSchedule(Base):
    __tablename__ = "payment_schedule"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)
    period: Mapped[str] = mapped_column(ForeignKey("pricing.period"), primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    paid: Mapped[str] = mapped_column(String, nullable=True)  # is a date

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id},year={self.year},amount={self.amount},paid={self.paid})"
