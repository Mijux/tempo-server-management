#!/usr/bin/env python3

from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from uuid import uuid4

from db.models.base import Base
from db.models.derogation import Derogation
from db.models.payment_schedule import PaymentSchedule
from db.models.user_presence_status import UserPresenceStatus

class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    permission_level: Mapped[int] = mapped_column(Integer, nullable=False)

    derogations: Mapped[List["Derogation"]] = relationship()
    payment_schedule: Mapped[List["PaymentSchedule"]] = relationship()
    user_presence_status: Mapped[List["UserPresenceStatus"]] = relationship()

    def __repr__(self) -> str:
        return f"User(id={self.id},username={self.username},avatar={self.avatar},permission_level={self.permission_level}"
