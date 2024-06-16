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
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, joinedload
from models import Prisoner, Gender, Crime, Prison, Base

# Constants
DB_CONNECTION_STRING = "sqlite:///database.db"


def _fk_pragma_on_connect(dbapi_con, con_record):
    """
    Ensure enforcement of foreign keys
    """

    dbapi_con.execute("pragma foreign_keys=ON")


def create_engine() -> Engine:
    """
    Creates and returns a new SQLAlchemy engine.

    Returns:
    Engine: The SQLAlchemy engine.
    """
    engine = sqlalchemy.create_engine(
        DB_CONNECTION_STRING,
    )

    # Make sure foreign keys are enforced
    event.listen(engine, "connect", _fk_pragma_on_connect)

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

    Base.metadata.create_all(db_engine)

    session = create_session()

    try:
        # Load Genders
        genders = data_frame["gender"].unique()
        for gender in genders:
            gender_record = Gender(title=gender)
            session.add(gender_record)
        session.commit()

        # Load Crimes
        crimes = data_frame["crime"].unique()
        for crime in crimes:
            crime_record = Crime(name=crime)
            session.add(crime_record)
        session.commit()

        # Load Prisons
        prisons = data_frame["prison"].unique()
        for prison in prisons:
            prison_record = Prison(name=prison)
            session.add(prison_record)
        session.commit()

        # Map IDs
        gender_map = {g.title: g.id for g in session.query(Gender).all()}
        crime_map = {c.name: c.id for c in session.query(Crime).all()}
        prison_map = {p.name: p.id for p in session.query(Prison).all()}

        # Prepare prisoner data with mapped IDs
        prisoner_data = []
        for _, row in data_frame.iterrows():
            prisoner_data.append(
                {
                    "prisoner_id": row["prisoner_id"],
                    "name": row["name"],
                    "age": row["age"],
                    "gender_id": gender_map[row["gender"]],
                    "crime_id": crime_map[row["crime"]],
                    "sentence_years": row["sentence_years"],
                    "prison_id": prison_map[row["prison"]],
                }
            )

        prisoners_df = pd.DataFrame(prisoner_data)

        prisoners_df.to_sql(
            name="prisoners", con=db_engine, if_exists="replace", index=False
        )
    finally:
        session.close()
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
            session.query(Prisoner)
            .options(
                joinedload(Prisoner.gender),
                joinedload(Prisoner.crime),
                joinedload(Prisoner.prison),
            )
            .filter_by(prisoner_id=prisoner_id)
            .one_or_none()
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
        query = session.query(Prisoner).options(
            joinedload(Prisoner.gender),
            joinedload(Prisoner.crime),
            joinedload(Prisoner.prison),
        )
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
        prisoners = (
            session.query(Prisoner)
            .options(
                joinedload(Prisoner.gender),
                joinedload(Prisoner.crime),
                joinedload(Prisoner.prison),
            )
            .all()
        )

        # Convert the list of Prisoner objects to a list of presentable JSON objects
        prisoners_data = [prisoner.to_json() for prisoner in prisoners]

        # Remove the SQLAlchemy _sa_instance_state entry
        for data in prisoners_data:
            data.pop("_sa_instance_state", None)

        return pd.DataFrame(prisoners_data)
    finally:
        session.close()
