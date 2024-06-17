#!/usr/bin/env python3

"""
File Name: models.py
Description: This file contains ORM class definitions for the database.
Author: Jack Gilmore
Date: 2024-06-13
"""

from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()


class Gender(Base):
    __tablename__ = "gender"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class Crime(Base):
    __tablename__ = "crime"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Prison(Base):
    __tablename__ = "prison"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Prisoner(Base):
    __tablename__ = "prisoners"

    prisoner_id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(BigInteger, nullable=False)
    gender_id = Column(Integer, ForeignKey("gender.id"), nullable=False)
    crime_id = Column(Integer, ForeignKey("crime.id"), nullable=False)
    sentence_years = Column(Integer, nullable=False)
    prison_id = Column(Integer, ForeignKey("prison.id"), nullable=False)

    gender = relationship("Gender", back_populates="prisoners")
    crime = relationship("Crime", back_populates="prisoners")
    prison = relationship("Prison", back_populates="prisoners")

    def to_json(self):
        return {
            "prisoner_id": self.prisoner_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender.title,
            "crime": self.crime.name,
            "sentence_years": self.sentence_years,
            "prison": self.prison.name,
        }

    def to_out(self):
        return Prisoner_Out(self)

class Prisoner_Out(BaseModel):
    prisoner_id: int
    name: str
    age: int
    gender: str
    crime: str
    sentence_years: int
    prison: str

    def __init__(self, prisoner: Prisoner):
        self.prisoner_id = prisoner.prisoner_id
        self.name = prisoner.name
        self.age = prisoner.age
        self.gender = prisoner.gender.title
        self.crime = prisoner.crime.name
        self.sentence_years = prisoner.sentence_years
        self.prison = prisoner.prison.name


Gender.prisoners = relationship(
    "Prisoner", order_by=Prisoner.prisoner_id, back_populates="gender"
)
Crime.prisoners = relationship(
    "Prisoner", order_by=Prisoner.prisoner_id, back_populates="crime"
)
Prison.prisoners = relationship(
    "Prisoner", order_by=Prisoner.prisoner_id, back_populates="prison"
)
