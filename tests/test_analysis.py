#!/usr/bin/env python3

"""
Script Name: test_analysis.py
Description: This script is to test analysis.py functions
Author: Jack Gilmore
Date: 2024-06-17
"""

import pytest
import pandas as pd
import sys
import os

# Get the current directory of this script
current_dir = os.path.dirname(__file__)

# Add the 'src' directory to the sys.path
src_dir = os.path.join(current_dir, "..", "src")
sys.path.insert(0, src_dir)

# Import analysis.py from src
from analysis import (
    prisoners_by_crime_type,
    average_sentence_length,
    average_sentence_length_by_crime_type,
    gender_distribution,
    prisoners_by_prison,
    age_distribution,
)

# ARRANGE: Sample data for testing
sample_data = pd.DataFrame(
    [
        {
            "prisoner_id": 1,
            "crime": "Theft",
            "sentence_years": 12,
            "gender": "Male",
            "prison": "Edinburgh",
            "age": 35,
        },
        {
            "prisoner_id": 2,
            "crime": "Assault",
            "sentence_years": 8,
            "gender": "Female",
            "prison": "Glasgow",
            "age": 28,
        },
        {
            "prisoner_id": 3,
            "crime": "Robbery",
            "sentence_years": 15,
            "gender": "Male",
            "prison": "Aberdeen",
            "age": 42,
        },
        {
            "prisoner_id": 4,
            "crime": "Theft",
            "sentence_years": 10,
            "gender": "Female",
            "prison": "Edinburgh",
            "age": 30,
        },
        {
            "prisoner_id": 5,
            "crime": "Assault",
            "sentence_years": 7,
            "gender": "Male",
            "prison": "Glasgow",
            "age": 25,
        },
    ]
)


def test_prisoners_by_crime_type():
    # ACT
    result = prisoners_by_crime_type(sample_data)

    # Set the index to 'crime'
    result = result.set_index("crime")

    # ASSERT
    expected_theft_prisoners = 2
    expected_assault_prisoners = 2
    expected_robbery_prisoners = 1
    expected_crime_types_count = 3

    assert result.loc["Theft", "count"] == expected_theft_prisoners
    assert result.loc["Assault", "count"] == expected_assault_prisoners
    assert result.loc["Robbery", "count"] == expected_robbery_prisoners
    assert len(result) == expected_crime_types_count


def test_average_sentence_length():
    # ACT
    result = average_sentence_length(sample_data)

    # ASSERT
    expected_average_sentence_length = 10.4
    assert result == expected_average_sentence_length


def test_average_sentence_length_by_crime_type():
    # ACT
    result = average_sentence_length_by_crime_type(sample_data)

    # Set the index to 'crime'
    result = result.set_index("crime")

    # ASSERT
    expected_theft_sentence = 11.0
    expected_theft_sentence_formatted = "11 years"
    expected_assault_sentence = 7.5
    expected_assault_sentence_formatted = "7 years and 6 months"
    expected_robbery_sentence = 15
    expected_robbery_sentence_formatted = "15 years"
    expected_crime_types_count = 3

    assert result.loc["Theft", "average_sentence_years"] == expected_theft_sentence
    assert result.loc["Theft", "average_sentence"] == expected_theft_sentence_formatted
    assert result.loc["Assault", "average_sentence_years"] == expected_assault_sentence
    assert (
        result.loc["Assault", "average_sentence"] == expected_assault_sentence_formatted
    )
    assert result.loc["Robbery", "average_sentence_years"] == expected_robbery_sentence
    assert (
        result.loc["Robbery", "average_sentence"] == expected_robbery_sentence_formatted
    )
    assert len(result) == expected_crime_types_count


def test_gender_distribution():
    # ACT
    result = gender_distribution(sample_data)

    # Set the index to 'gender'
    result = result.set_index("gender")

    # ASSERT
    expected_male_count = 3
    expected_female_count = 2

    assert result.loc["Male", "count"] == expected_male_count
    assert result.loc["Female", "count"] == expected_female_count


def test_prisoners_by_prison():
    # ACT
    result = prisoners_by_prison(sample_data)

    # Set the index to 'prison'
    result = result.set_index("prison")

    # ASSERT
    expected_edinburgh_count = 2
    expected_glasgow_count = 2
    expected_aberdeen_count = 1

    assert result.loc["Edinburgh", "count"] == expected_edinburgh_count
    assert result.loc["Glasgow", "count"] == expected_glasgow_count
    assert result.loc["Aberdeen", "count"] == expected_aberdeen_count


def test_age_distribution():
    # ACT
    result = age_distribution(sample_data)

    # Set the index to 'age'
    result = result.set_index("age")

    # ASSERT
    expected_16_to_17 = 0
    expected_25_to_29 = 2
    expected_30_to_34 = 1

    assert result.loc["16-17", "count"] == expected_16_to_17
    assert result.loc["25-29", "count"] == expected_25_to_29
    assert result.loc["30-34", "count"] == expected_30_to_34
