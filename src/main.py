#!/usr/bin/env python3

"""
Script Name: main.py
Description: This script runs the REST API to serve the prisoner data
Author: Jack Gilmore
Date: 2024-06-12
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import database
from models import Prisoner, Base

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

@app.get("/api/helloworld/{name}")
async def hello_world(name: str, authenticated: bool = Depends(authenticate_user)) -> dict:
    """
    Output a message, telling the person hello

    Parameters:
    name: A string with a person's name

    Returns:
    dict: A dict to be used as a JSON message
    """

    return {"message": f"Hello {name}"}

@app.get("/api/prisoners/{prisoner_id}")
async def prisoner_by_id(prisoner_id: int, authenticated: bool = Depends(authenticate_user)):
    prisoner = database.get_prisoner_by_id(prisoner_id)
    if prisoner:
        return prisoner
    else:
        raise HTTPException(status_code=404, detail="Prisoner not found")

# Mount static files folder for dashboard
# NOTE: Static file mount must come last 
app.mount("/", StaticFiles(directory="static", html=True), name="static")