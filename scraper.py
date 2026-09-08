

from app.database import save_policies
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.config import BASE_URL, POLICIES_URL



# Fetch webpage HTML


def fetch_page(url):
    """
    Download webpage HTML.
    """

    try:

        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        return response.text


    except requests.RequestException as error:

        print(
            f"Request failed: {error}"
        )

        return None



# Scrape Policies Table

def scrape_policies():

    html = fetch_page(
        POLICIES_URL
    )


    policies = []


    if not html:

        return policies



    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    table = soup.find(
        "table",
        id="myTable"
    )


    if not table:

        print(
            "Table not found"
        )

        return policies



    rows = table.find_all(
        "tr"
    )



    for row in rows:


        columns = row.find_all(
            "td"
        )



        if len(columns) < 4:

            continue



        # SR NO


        sr_no = columns[0].get_text(
            strip=True
        )



        # TITLE + DETAIL URL

        title = ""

        detail_url = None


        title_link = columns[1].find(
            "a",
            href=True
        )


        if title_link:

            title = title_link.get_text(
                strip=True
            )


            detail_url = urljoin(
                BASE_URL,
                title_link["href"]
            )



        # DATE

        date = columns[2].get_text(
            strip=True
        )



        # PDF URL

        pdf_url = None


        pdf_link = columns[3].find(
            "a",
            href=True
        )


        if pdf_link:

            pdf_url = urljoin(
                BASE_URL,
                pdf_link["href"]
            )



        policies.append(
            {
                "sr_no": sr_no,
                "title": title,
                "date": date,
                "detail_url": detail_url,
                "pdf_url": pdf_url
            }
        )



    return policies




def main():

    print(
        "Cabinet Scraper Started"
    )


    policies = scrape_policies()


    print(
        f"Policies Found: {len(policies)}"
    )


    print(
        "\nSample Records:\n"
    )


    for policy in policies[:5]:

        print(policy)

        print()

    print("\nSaving to MongoDB...")

    save_policies(policies)




# Entry Point

if __name__ == "__main__":

    main()