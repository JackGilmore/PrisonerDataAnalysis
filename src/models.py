#!/usr/bin/env python3

"""
File Name: models.py
Description: This file contains ORM class definitions for the database.
Author: Jack Gilmore
Date: 2024-06-13
"""

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prisoner(Base):
    __tablename__ = "prisoners"
    
    prisoner_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    age = Column(BigInteger)
    gender = Column(String)
    crime = Column(String)
    sentence_years = Column(BigInteger)
    prison = Column(String)