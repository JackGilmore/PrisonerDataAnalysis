#!/usr/bin/env python3

"""
Script Name: analysis.py
Description: This script performs basic data analysis to extract insights, such as the number of prisoners by crime type, average sentence length, and gender distribution
Author: Jack Gilmore
Date: 2024-06-12
"""

import logging
import pandas as pd


def perform_analysis(data_frame: pd.DataFrame):
    logging.info("Performing analysis")

    prisoners_by_crime_type(data_frame)


def prisoners_by_crime_type(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Analyses the number of prisoners by crime type.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.DataFrame: A DataFrame with the count of prisoners for each crime type.
    """

    # Group by crime column and get prisoner counts
    prisoners_by_crime_type = (
        data_frame.groupby("crime").size().reset_index(name="count")
    )

    # Sort the results
    prisoners_by_crime_type = prisoners_by_crime_type.sort_values(by="count", ascending=False).reset_index(drop=True)

    logging.info(f"Prisoners by crime type")
    logging.info(f"\n{prisoners_by_crime_type.to_string(index=False)}")


def average_sentence_length(data_frame: pd.DataFrame) -> float:
    """
    Calculates the average sentence length.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    float: The average sentence length.
    """


def gender_distribution(data_frame: pd.DataFrame) -> pd.Series:
    """
    Analyses the gender distribution of prisoners.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.Series: A Series with the count of prisoners for each gender.
    """


def prisoners_by_prison(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Analyses the number of prisoners by prison.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.DataFrame: A DataFrame with the count of prisoners for each prison.
    """


def age_distribution(data_frame: pd.DataFrame) -> pd.Series:
    """
    Analyses the age distribution of prisoners.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.Series: A Series with the distribution of ages.
    """
