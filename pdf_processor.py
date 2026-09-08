"""
Cabinet Division PDF Processor

This module:

1. Reads PDFs from pdfs folder.
2. Extracts text.
3. Saves Markdown files.
4. Updates MongoDB records.
"""

from pathlib import Path
import re

from pypdf import PdfReader

from app.config import PDF_FOLDER, MARKDOWN_FOLDER
from app.database import get_database


# --------------------------------------------------
# Create comparable filename
# --------------------------------------------------

def clean_name(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        "_",
        text
    )

    return text.strip("_")


# --------------------------------------------------
# Extract PDF text
# --------------------------------------------------

def extract_text_from_pdf(pdf_path):

    try:

        reader = PdfReader(
            str(pdf_path)
        )

        text = ""


        for page in reader.pages:

            content = page.extract_text()

            if content:

                text += content + "\n"


        return text.strip()


    except Exception as error:

        print(
            f"Extraction error: {pdf_path.name}"
        )

        print(error)

        return None



# --------------------------------------------------
# Save markdown file
# --------------------------------------------------

def save_markdown(pdf_path, text):

    markdown_path = (
        MARKDOWN_FOLDER /
        f"{pdf_path.stem}.md"
    )


    with open(
        markdown_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            f"# {pdf_path.stem}\n\n"
        )

        file.write(text)


    return markdown_path



# --------------------------------------------------
# Update MongoDB record
# --------------------------------------------------

def update_database(
        collection,
        pdf_path,
        markdown_path
):

    filename = clean_name(
        pdf_path.stem
    )


    records = collection.find()


    for record in records:


        title = clean_name(
            record.get("title", "")
        )


        if title == filename:


            collection.update_one(

                {
                    "_id": record["_id"]
                },

                {
                    "$set":
                    {
                        "pdf_file": str(pdf_path),
                        "markdown_file": str(markdown_path)
                    }
                }

            )


            return True



    return False



# --------------------------------------------------
# Process PDFs
# --------------------------------------------------

def process_pdfs():

    print(
        "PDF Processor Started"
    )


    collection = get_database()


    if collection is None:

        return



    pdf_files = list(
        PDF_FOLDER.glob("*.pdf")
    )


    print(
        f"PDF Files Found: {len(pdf_files)}"
    )


    processed = 0



    for pdf_file in pdf_files:


        print(
            f"Processing: {pdf_file.name}"
        )


        text = extract_text_from_pdf(
            pdf_file
        )


        if not text:


            print(
                "No text extracted"
            )


            print(
                "---------------------"
            )


            continue



        markdown_file = save_markdown(
            pdf_file,
            text
        )


        updated = update_database(

            collection,

            pdf_file,

            markdown_file
        )



        if updated:

            print(
                "Database Updated"
            )


        else:

            print(
                "Database record not matched"
            )


        processed += 1


        print(
            "---------------------"
        )



    print(
        f"Completed. Processed {processed} PDFs"
    )



# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    process_pdfs()