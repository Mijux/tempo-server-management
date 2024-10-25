#!/usr/bin/env python3

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from models.base import Base
from utils.singleton import SingletonMeta


class EngineSingleton(metaclass=SingletonMeta):
    engine: Engine = None
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self, engine_parameters: str = None) -> None:
        if not self.engine:
            if not engine_parameters:
                engine_parameters = "sqlite:///database.db"
            self.engine = create_engine(engine_parameters, echo=False)

    def get_engine(self) -> Engine:
        return self.engine


def init_db():
    Base.metadata.create_all(EngineSingleton().get_engine())


def get_session():
    return Session(EngineSingleton().get_engine())
