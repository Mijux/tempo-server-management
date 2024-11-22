#!/usr/bin/env python3

from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from uuid import uuid4

from models.base import Base


class Derogation(Base):
    __tablename__ = "derogation"

    date: Mapped[str] = mapped_column(ForeignKey("day.date"), primary_key=True)
    id_user: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)

    def __repr__(self) -> str:
        return f"Derogation(id_user={self.id_user},date={self.date})"
