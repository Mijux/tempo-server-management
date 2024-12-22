#!/usr/bin/env python3

from typing import List
from sqlalchemy import Date, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from uuid import uuid4

from db.models.base import Base


class UserPresenceStatus(Base):
    __tablename__ = "user_presence_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_user: Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    arrival_date: Mapped[str] = mapped_column(Date, nullable=False)
    leave_date: Mapped[str] = mapped_column(Date, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id},id_user={self.id_user},arrival_date={self.arrival_date},leave_date={self.leave_date}"
