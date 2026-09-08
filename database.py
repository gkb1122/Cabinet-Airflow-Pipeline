"""
MongoDB Database Handler for Cabinet Scraper

This module:

1. Connects to MongoDB.
2. Creates/uses cabinet database.
3. Creates/uses policies collection.
4. Inserts scraped policy records.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from app.config import (
    MONGO_URI,
    DATABASE_NAME,
    COLLECTION_NAME
)


# --------------------------------------------------
# MongoDB Connection
# --------------------------------------------------

def get_database():

    try:

        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        # Test connection
        client.admin.command("ping")

        print("MongoDB Connected Successfully")

        db = client[DATABASE_NAME]

        collection = db[COLLECTION_NAME]

        return collection


    except ConnectionFailure as error:

        print(
            f"MongoDB Connection Failed: {error}"
        )

        return None



# --------------------------------------------------
# Insert Policies
# --------------------------------------------------

def save_policies(policies):

    collection = get_database()


    if collection is None:

        return False



    if not policies:

        print(
            "No policies to insert"
        )

        return False



    try:

        result = collection.insert_many(
            policies
        )


        print(
            f"Inserted {len(result.inserted_ids)} records into MongoDB"
        )


        return True



    except Exception as error:

        print(
            f"Insert failed: {error}"
        )

        return False



# --------------------------------------------------
# Test Run
# --------------------------------------------------

if __name__ == "__main__":

    print(
        "Database Test Started"
    )


    collection = get_database()


    if collection is not None:

        print(
            "Database Ready"
        )