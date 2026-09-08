"""
Configuration file for Cabinet Scraper project.

Stores:

- Website URLs
- Project paths
- MongoDB settings
- Environment variables
"""


import os
from pathlib import Path
from dotenv import load_dotenv



# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()



# --------------------------------------------------
# Project Paths
# --------------------------------------------------

# Main project directory

BASE_DIR = Path(__file__).resolve().parent.parent



# Storage folders

PDF_FOLDER = BASE_DIR / "pdfs"

MARKDOWN_FOLDER = BASE_DIR / "markdown"

LOG_FOLDER = BASE_DIR / "logs"



# Create folders if they do not exist

PDF_FOLDER.mkdir(
    exist_ok=True
)

MARKDOWN_FOLDER.mkdir(
    exist_ok=True
)

LOG_FOLDER.mkdir(
    exist_ok=True
)



# --------------------------------------------------
# Website Configuration
# --------------------------------------------------

BASE_URL = "https://cabinet.gov.pk"


POLICIES_URL = f"{BASE_URL}/Policies"



# --------------------------------------------------
# MongoDB Configuration
# --------------------------------------------------

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)


DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "cabinet_db"
)


COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "laws"
)