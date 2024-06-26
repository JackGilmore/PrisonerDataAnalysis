#!/usr/bin/env python3

"""
Script Name: main.py
Description: This script runs the REST API to serve the prisoner data
Author: Jack Gilmore
Date: 2024-06-12
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import analysis
import database
from models import Prisoner, Prisoner_Out, Base
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Retrieve the username and password from environment variables
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

# Create an instance of the FastAPI class
app = FastAPI()

# Create an instance of the HTTPBasic class
security = HTTPBasic()


# Define a function to authenticate users
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect credentials supplied")
    return True


@app.get("/api/prisoners/{prisoner_id}")
async def prisoner_by_id(
    prisoner_id: int, authenticated: bool = Depends(authenticate_user)
) -> Prisoner_Out:
    prisoner = database.get_prisoner_by_id(prisoner_id)
    if prisoner:
        return prisoner.to_out()
    else:
        raise HTTPException(status_code=404, detail="Prisoner not found")


@app.get("/api/prisoners")
@app.get("/api/prisoners/", include_in_schema=False)
def read_prisoners(
    page: Optional[int] = Query(None, gt=0),
    per_page: Optional[int] = Query(None, gt=0),
    authenticated: bool = Depends(authenticate_user),
) -> list[Prisoner_Out]:
    prisoners = database.get_paginated_prisoners(page, per_page)

    if prisoners is None:
        raise HTTPException(status_code=404, detail="Prisoners not found")

    return list(map(lambda prisoners: prisoners.to_out(), prisoners))


@app.get("/api/analysis")
@app.get("/api/analysis/", include_in_schema=False)
def analysis_output():
    prisoners = database.get_all_prisoners_as_dataframe()

    if prisoners is None:
        raise HTTPException(status_code=404, detail="Prisoners not found")

    summary_analysis = analysis.perform_analysis(prisoners)

    return summary_analysis


# Mount static files folder for dashboard
# NOTE: Static file mount must come last
app.mount("/", StaticFiles(directory="static", html=True), name="static")
