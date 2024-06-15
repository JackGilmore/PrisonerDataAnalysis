#!/usr/bin/env python3

"""
Script Name: database.py
Description: This script is used for database connectivity
Author: Jack Gilmore
Date: 2024-06-13
"""

import logging
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from models import Prisoner, Base

# Constants
DB_CONNECTION_STRING = "sqlite:///database.db"


def create_engine() -> Engine:
    """
    Creates and returns a new SQLAlchemy engine.

    Returns:
    Engine: The SQLAlchemy engine.
    """
    return sqlalchemy.create_engine(DB_CONNECTION_STRING)


def create_session() -> Session:
    """
    Creates and returns a new SQLAlchemy session.

    Returns:
    Session: A new SQLAlchemy session.
    """

    db_engine = create_engine()
    Session = sessionmaker(bind=db_engine)
    return Session()


def load_data_frame_to_database(data_frame: pd.DataFrame) -> None:
    """
    Loads the DataFrame into an SQLite database file

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.
    """

    db_engine = create_engine()

    try:
        data_frame = data_frame.set_index("prisoner_id")

        data_frame.to_sql(name="prisoners", con=db_engine, if_exists="replace")
    finally:
        db_engine.dispose()


def get_prisoner_by_id(prisoner_id: int) -> Prisoner:
    """
    Get a single prisoner record by prisoner_id

    Parameters:
    prisoner_id (int): The prisoner ID to query.

    Returns:
    Prisoner: The prisoner record.
    """

    session = create_session()

    try:
        prisoner = (
            session.query(Prisoner).filter_by(prisoner_id=prisoner_id).one_or_none()
        )
        return prisoner
    finally:
        session.close()


def get_paginated_prisoners(page: int = None, per_page: int = None) -> list[Prisoner]:
    """
    Get a paginated list of prisoners or all prisoners if no pagination parameters are provided.

    Parameters:
    page (int, optional): The page number (1-based). Defaults to None.
    per_page (int, optional): The number of records per page. Defaults to None.

    Returns:
    list[Prisoner]: A list of prisoners for the specified page or all prisoners.
    """

    session = create_session()

    try:
        query = session.query(Prisoner)
        if page is not None and per_page is not None:
            offset = (page - 1) * per_page
            prisoners = query.offset(offset).limit(per_page).all()
        else:
            prisoners = query.all()
        return prisoners
    finally:
        session.close()


def get_all_prisoners_as_dataframe() -> pd.DataFrame:
    """
    Fetches all prisoners and returns them as a pandas DataFrame.

    Returns:
    pd.DataFrame: DataFrame containing all prisoners.
    """

    session = create_session()

    try:
        prisoners = session.query(Prisoner).all()

        # Convert the list of Prisoner objects to a list of dictionaries
        prisoners_data = [prisoner.__dict__ for prisoner in prisoners]

        # Remove the SQLAlchemy _sa_instance_state entry
        for data in prisoners_data:
            data.pop("_sa_instance_state", None)

        return pd.DataFrame(prisoners_data)
    finally:
        session.close()
