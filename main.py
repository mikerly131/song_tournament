"""
A simple, basic FastAPI web application for creating bracket's for best item tournaments
First iteration will only be for songs only.

Many comments to explain what code is doing, this web app is for beginners to reference
"""
from dotenv import load_dotenv

# Load env variables
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import index, account, bracket


# Create the FastAPI app
app = FastAPI(docs_url=None, redoc_url=None)

# Include the CSS/JS in static by mounting to the app
app.mount('/static', StaticFiles(directory='static'), name='static')

# Include the routers for the routes, make sure to import the files
app.include_router(index.router)
app.include_router(account.router)
app.include_router(bracket.router)
