#!/usr/bin/env python3

"""
Script Name: analysis.py
Description: This script performs basic data analysis to extract insights, such as the number of prisoners by crime type, average sentence length, and gender distribution
Author: Jack Gilmore
Date: 2024-06-12
"""

import logging
import pandas as pd


def years_number_to_formatted_string(years_number: float) -> str:
    """
    Takes a float number and converts it to "x years and y months" where applicable

    Parameters:
    years_number (float): The number of years as a floating point number

    Returns:
    str: A formatted string of years and months where applicable
    """
    years = int(years_number)
    months = (years_number - years) * 12
    months = int(round(months))

    formatted_string = ""

    if years > 0:
        formatted_string += f"{years} years"

    if months > 0 and years > 0:
        formatted_string += " and "

    if months > 0:
        formatted_string += f"{months} months"

    return formatted_string


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

    # Sort the results alphabetically by crime
    prisoners_by_crime_type = prisoners_by_crime_type.sort_values(
        by="crime", ascending=True
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
    formatted_average_sentence_length = years_number_to_formatted_string(
        average_sentence_length
    )

    logging.info(f"Average sentence length: {formatted_average_sentence_length}")

    return average_sentence_length


def average_sentence_length_by_crime_type(data_frame) -> pd.DataFrame:
    """
    Analyses the average sentence length by crime type.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.DataFrame: A DataFrame with crime types and their corresponding average sentence lengths
                  in years and in a readable "years and months" format.
    """
    sentence_length_by_crime_type = (
        data_frame.groupby("crime")["sentence_years"].mean().reset_index()
    )
    sentence_length_by_crime_type.columns = ["crime", "average_sentence_years"]

    # Convert average sentence length to years and months
    sentence_length_by_crime_type["average_sentence"] = sentence_length_by_crime_type[
        "average_sentence_years"
    ].apply(lambda x: f"{years_number_to_formatted_string(x)}")

    # Sort the results alphabetically by crime
    sentence_length_by_crime_type = sentence_length_by_crime_type.sort_values(
        by="crime", ascending=True
    ).reset_index(drop=True)

    logging.info(f"Average sentence length by crime type")
    logging.info(f"\n{sentence_length_by_crime_type.to_string(index=False)}")

    return sentence_length_by_crime_type


def gender_distribution(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Analyses the gender distribution of prisoners.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.DataFrame: A DataFrame with the count of prisoners for each gender.
    """

    # Group by gender column and get prisoner counts
    prisoners_by_gender = data_frame.groupby("gender").size().reset_index(name="count")

    # Sort the results
    prisoners_by_gender = prisoners_by_gender.sort_values(
        by="count", ascending=False
    ).reset_index(drop=True)

    logging.info(f"Gender distribution")
    logging.info(f"\n{prisoners_by_gender.to_string(index=False)}")

    return prisoners_by_gender


def gender_distribution_by_crime_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the distribution of genders for each type of crime.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.DataFrame: A DataFrame with the distribution of genders for each type of crime.
    """

    # Group by crime type and gender, then count occurrences
    gender_distribution_by_crime = (
        df.groupby(["crime", "gender"]).size().unstack(fill_value=0)
    )

    # Sort the results
    gender_distribution_by_crime = gender_distribution_by_crime.sort_values(
        by="crime", ascending=True
    )

    logging.info(f"Gender distribution by crime type")
    logging.info(f"\n{gender_distribution_by_crime}")

    return gender_distribution_by_crime


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

    # Sort the results alphabetically by prison
    prisoners_by_prison = prisoners_by_prison.sort_values(
        by="prison", ascending=True
    ).reset_index(drop=True)

    logging.info(f"Prisoners by prison")
    logging.info(f"\n{prisoners_by_prison.to_string(index=False)}")

    return prisoners_by_prison


def age_distribution(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Analyses the age distribution of prisoners.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns:
    pd.DataFrame: A DataFrame with the distribution of ages.
    """

    # Using age bands as defined in Scottish prison population statistics technical manual
    # https://www.gov.scot/publications/scottish-prison-population-statistics/pages/analytical-factors-and-measurements/#Age%20Bands

    # Define the bin edges and labels
    bin_edges = [
        0,
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
        "Under 16",
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
    age_bins = pd.cut(data_frame["age"], bins=bin_edges, labels=bin_labels, right=True)

    # Count the number of occurrences in each bin
    age_distribution = (
        age_bins.value_counts().sort_index().rename("count").reset_index()
    )
    age_distribution = age_distribution.rename(columns={"index": "age_group"})

    logging.info(f"Age distribution")
    logging.info(f"\n{age_distribution.to_string(index=False)}")

    return age_distribution


def dataframe_to_oriented_dict(data_frame: pd.DataFrame, orient_direction="records") -> dict:
    """
    Converts a DataFrame to a dict oriented by records

    Parameters:
    data_frame (pd.DataFrame): The DataFrame.

    Returns
    dict: A dict oriented by records
    """
    return data_frame.to_dict(orient=orient_direction)


def perform_analysis(data_frame: pd.DataFrame) -> dict:
    """
    Performs a range of basic analysis on the prisoner dataset

    Parameters:
    data_frame (pd.DataFrame): The DataFrame containing prisoner data.

    Returns
    dict: A dict of all the analysis statistics
    """

    logging.info("Performing analysis")

    prisoners_by_crime_type_stat = prisoners_by_crime_type(data_frame)

    average_sentence_length_stat = average_sentence_length(data_frame)

    average_sentence_length_by_crime_type_stat = average_sentence_length_by_crime_type(
        data_frame
    )

    gender_distribution_stat = gender_distribution(data_frame)

    gender_distribution_by_crime_type_stat = gender_distribution_by_crime_type(data_frame)

    prisoners_by_prison_stat = prisoners_by_prison(data_frame)

    age_distribution_stat = age_distribution(data_frame)

    return {
        "prisoners_by_crime_type": dataframe_to_oriented_dict(
            prisoners_by_crime_type_stat
        ),
        "average_sentence_length": average_sentence_length_stat,
        "average_sentence_length_by_crime_type": dataframe_to_oriented_dict(
            average_sentence_length_by_crime_type_stat
        ),
        "gender_distribution": dataframe_to_oriented_dict(gender_distribution_stat),
        "gender_distribution_by_crime_type": dataframe_to_oriented_dict(gender_distribution_by_crime_type_stat, "index"),
        "prisoners_by_prison": dataframe_to_oriented_dict(prisoners_by_prison_stat),
        "age_distribution": dataframe_to_oriented_dict(age_distribution_stat),
    }
