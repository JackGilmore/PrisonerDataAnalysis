#!/usr/bin/env python3

"""
Script Name: load_data.py
Description: This script loads and manipulates the prisoner dataset using Pandas.
Author: Jack Gilmore
Date: 2024-06-11
"""

import os
import sys
import logging
import pymupdf
import pandas as pd
import analysis
from io import StringIO
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
DATA_SOURCE_NAME = "coding-test.pdf"
DATASET_HEADER = "prisoner_id,name,age,gender,crime,sentence_years,prison"


def load_data() -> list:
    """
    Loads the data from the PDF, extracts the text and truncates the text lines down to the relevant dataset

    Returns:
    list: A string array of the dataset with each item a comma separated string for a row in the dataset
    """

    logging.info(f"Opening {DATA_SOURCE_NAME}")

    # Build the base path using the folder our script lives in
    script_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    data_source_path = os.path.join(script_path, DATA_SOURCE_NAME)

    # Open the document
    data_source_document = None
    try:
        data_source_document = pymupdf.open(data_source_path)
    except pymupdf.FileNotFoundError:
        logging.error(f"Could not find file at path {data_source_path}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    # If we couldn't read the file for some reason, error out gracefully
    if data_source_document == None:
        sys.exit(1)

    data_source_lines = []

    logging.info(f"Extracting text from {DATA_SOURCE_NAME}")

    # Loop through the pages, skipping the first one as it contains no relevant content to scrape
    for page in data_source_document[1:]:
        # Get plain text encoded as UTF-8
        page_text = page.get_text()

        # Split text by newlines and strip whitespace
        page_lines = [line.strip() for line in str.splitlines(page_text)]

        # Add the lines to our full list of document lines
        data_source_lines += page_lines

    line_count = len(data_source_lines)

    logging.info(f"Line count: {line_count}")

    logging.info("Finding start of dataset")

    # Find the text with the header for the CSV
    # We want to ignore any text before this as it isn't data. Just instructions.
    header_index = next(
        (
            index
            for index, line_string in enumerate(data_source_lines)
            if DATASET_HEADER in line_string
        ),
        -1,
    )

    # If we don't get a header back, error out gracefully
    if header_index == -1:
        logging.error(f"Could not find a header row with value of {DATASET_HEADER}")
        sys.exit(1)

    logging.info(f"Header index found at {header_index}")

    # Truncate our PDF lines down to just the ones from the header onwards
    data_source = data_source_lines[header_index:]

    data_source_count = len(data_source)

    logging.info(
        f"Successfully retrieved {data_source_count} rows for dataset (including header)"
    )

    return data_source


def data_to_pandas(data: List[str]) -> pd.DataFrame:
    """
    Convert the raw dataset to a pandas DataFrame

    Parameters:
    data: An array of comma separated strings

    Returns:
    pd.DataFrame: A pandas DataFrame of the dataset
    """

    logging.info("Converting data to CSV file")

    data_as_csv_string = "\n".join(data)

    csv_file = StringIO(data_as_csv_string)

    logging.info("Reading CSV file into Pandas")

    data_frame = pd.read_csv(csv_file)

    logging.info(f"\n{data_frame}")

    return data_frame


def main(args: List[str]) -> None:
    """
    Main function that orchestrates the script's functionality.

    Parameters:
    args: A list of arguments
    """

    logging.info("Starting processing...")

    # Extract from PDF and load as an array of comma separated strings
    raw_dataset = load_data()

    # Convert the raw dataset to a Pandas DataFrame
    data_frame = data_to_pandas(raw_dataset)

    # Perform basic analysis
    analysis.perform_analysis(data_frame)


if __name__ == "__main__":
    main(sys.argv)
