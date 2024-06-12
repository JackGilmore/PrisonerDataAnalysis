#!/usr/bin/env python3

"""
Script Name: analysis.py
Description: This script performs basic data analysis to extract insights, such as the number of prisoners by crime type, average sentence length, and gender distribution
Author: Jack Gilmore
Date: 2024-06-12
"""

import logging
import pandas as pd

# Constants
GENDER_MAP = {"M": "Male", "F": "Female"}


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
    prisoners_by_crime_type = prisoners_by_crime_type.sort_values(
        by="count", ascending=False
    ).reset_index(drop=True)

    logging.info(f"Prisoners by crime type")
    logging.info(f"\n{prisoners_by_crime_type.to_string(index=False)}")

    return prisoners_by_crime_type


def average_sentence_length(data_frame: pd.DataFrame) -> float:
    """
    Calculates the average sentence length.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    float: The average sentence length.
    """

    # Get the average of the sentence_years column
    average_sentence_length = data_frame["sentence_years"].mean()

    # Convert the value to years and months
    years = int(average_sentence_length)
    months = (average_sentence_length - years) * 12
    months = int(round(months))

    logging.info(f"Average sentence length: {years} years and {months} months")

    return average_sentence_length


def gender_distribution(data_frame: pd.DataFrame) -> pd.Series:
    """
    Analyses the gender distribution of prisoners.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.Series: A Series with the count of prisoners for each gender.
    """

    # Group by gender column and get prisoner counts
    prisoners_by_gender = data_frame.groupby("gender").size().reset_index(name="count")

    # Sort the results
    prisoners_by_gender = prisoners_by_gender.sort_values(
        by="count", ascending=False
    ).reset_index(drop=True)

    # Remap the gender column with values that read better
    prisoners_by_gender["gender"] = prisoners_by_gender["gender"].map(GENDER_MAP)

    logging.info(f"Gender distribution")
    logging.info(f"\n{prisoners_by_gender.to_string(index=False)}")

    return prisoners_by_gender


def prisoners_by_prison(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Analyses the number of prisoners by prison.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.DataFrame: A DataFrame with the count of prisoners for each prison.
    """

    # Group by prison column and get prisoner counts
    prisoners_by_prison = data_frame.groupby("prison").size().reset_index(name="count")

    # Sort the results
    prisoners_by_prison = prisoners_by_prison.sort_values(
        by="count", ascending=False
    ).reset_index(drop=True)

    logging.info(f"Prisoners by prison")
    logging.info(f"\n{prisoners_by_prison.to_string(index=False)}")

    return prisoners_by_prison


def age_distribution(data_frame: pd.DataFrame) -> pd.Series:
    """
    Analyses the age distribution of prisoners.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.Series: A Series with the distribution of ages.
    """

    # Using age bands as defined in Scottish prison population statistics technical manual
    # https://www.gov.scot/publications/scottish-prison-population-statistics/pages/analytical-factors-and-measurements/#Age%20Bands

    # Define the bin edges and labels
    bin_edges = [
        16,
        17,
        20,
        22,
        24,
        29,
        34,
        39,
        44,
        49,
        54,
        59,
        64,
        69,
        74,
        float("inf"),
    ]
    bin_labels = [
        "16-17",
        "18-20",
        "21-22",
        "23-24",
        "25-29",
        "30-34",
        "35-39",
        "40-44",
        "45-49",
        "50-54",
        "55-59",
        "60-64",
        "65-69",
        "70-74",
        "75 or over",
    ]

    # Create the bins
    age_bins = pd.cut(data_frame["age"], bins=bin_edges, labels=bin_labels, right=False)

    # Count the number of occurrences in each bin
    age_distribution = (
        age_bins.value_counts().sort_index().rename("count").reset_index()
    )
    age_distribution = age_distribution.rename(columns={"index": "age_group"})

    logging.info(f"Age distribution")
    logging.info(f"\n{age_distribution.to_string(index=False)}")

    return age_distribution


def perform_analysis(data_frame: pd.DataFrame):
    """
    Performs a range of basic analysis on the prisoner dataset

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.
    """

    logging.info("Performing analysis")

    prisoners_by_crime_type(data_frame)

    average_sentence_length(data_frame)

    gender_distribution(data_frame)

    prisoners_by_prison(data_frame)

    age_distribution(data_frame)
