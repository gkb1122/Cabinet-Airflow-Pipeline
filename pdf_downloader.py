"""
Cabinet Division PDF Downloader

This module:

1. Reads policy records from MongoDB.
2. Downloads PDF files.
3. Saves them into the pdfs folder.
"""

import requests
from pathlib import Path

from app.database import get_database
from app.config import PDF_FOLDER


# --------------------------------------------------
# Download single PDF
# --------------------------------------------------

def download_pdf(pdf_url, file_path):
    """
    Download PDF from URL.

    Args:
        pdf_url (str): PDF URL
        file_path (Path): destination path

    Returns:
        bool
    """

    try:

        response = requests.get(
            pdf_url,
            timeout=60,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()


        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                response.content
            )


        return True


    except requests.RequestException as error:

        print(
            f"Download failed: {pdf_url}"
        )

        print(error)

        return False



# --------------------------------------------------
# Create safe filename
# --------------------------------------------------

def create_filename(title):
    """
    Convert title into filename.
    """

    filename = title.lower()

    filename = filename.replace(
        " ",
        "_"
    )


    invalid_chars = [
        "/",
        "\\",
        ":",
        "*",
        "?",
        "\"",
        "<",
        ">",
        "|"
    ]


    for char in invalid_chars:

        filename = filename.replace(
            char,
            ""
        )


    return filename + ".pdf"



# --------------------------------------------------
# Download all PDFs
# --------------------------------------------------

def download_all_pdfs():

    print(
        "PDF Downloader Started"
    )


    collection = get_database()


    if collection is None:

        print(
            "Database connection failed"
        )

        return



    policies = collection.find(
        {
            "pdf_url": {
                "$ne": None
            }
        }
    )


    count = 0


    for policy in policies:


        title = policy.get(
            "title"
        )


        pdf_url = policy.get(
            "pdf_url"
        )


        filename = create_filename(
            title
        )


        file_path = PDF_FOLDER / filename


        print(
            f"Downloading: {title}"
        )


        success = download_pdf(
            pdf_url,
            file_path
        )


        if success:

            print(
                "Saved:",
                file_path
            )

            count += 1


        print(
            "---------------------"
        )



    print(
        f"Completed. Downloaded {count} PDFs"
    )



# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    download_all_pdfs()