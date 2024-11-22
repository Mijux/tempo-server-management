#!/usr/bin/env python3

from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from uuid import uuid4

from models.base import Base


class UserPresenceStatus(Base):
    __tablename__ = "user_presence_status"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    id_user: Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    arrival_date: Mapped[str] = mapped_column(String, nullable=False)
    leave_date: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id},username={self.username},avatar={self.avatar},permission_level={self.permission_level},arrival_date={self.arrival_date},leave_date={self.leave_date})"
