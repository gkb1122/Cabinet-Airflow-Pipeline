

# Cabinet Scraper — Airflow Data Pipeline

An end-to-end **data engineering pipeline** that scrapes policies from the Government of Pakistan's Cabinet Division website, stores metadata in MongoDB, downloads policy PDFs, and converts text-extractable PDFs into Markdown files.

The pipeline is orchestrated using **Apache Airflow** and runs in a containerized environment using **Docker Compose**.

---

## 📌 Project Overview

The Cabinet Division publishes various government policies and documents online. This project automates the process of collecting and processing those documents.

The pipeline performs the following steps:

```text
Cabinet Division Website
          │
          ▼
     Web Scraper
          │
          ▼
       MongoDB
     Policy Metadata
          │
          ▼
    PDF Downloader
          │
          ▼
       PDF Files
          │
          ▼
    PDF Processor
          │
          ▼
   Markdown Files
```

Apache Airflow orchestrates these operations as dependent tasks:

```text
scrape_policies
       │
       ▼
download_pdfs
       │
       ▼
process_pdfs
```

---

## 🚀 Features

* Scrapes policy information from the Cabinet Division website
* Extracts:

  * Serial number
  * Policy title
  * Date
  * Detail URL
  * PDF URL
* Stores policy metadata in MongoDB
* Downloads policy PDFs automatically
* Extracts text from PDFs using `pypdf`
* Converts extracted PDF text into Markdown
* Updates MongoDB with generated PDF and Markdown file paths
* Uses Apache Airflow for workflow orchestration
* Uses Docker Compose for the Airflow environment
* Uses persistent local folders for PDFs and Markdown files
* Supports manual Airflow DAG execution
* Provides Airflow task-level monitoring and logs

---

## 🛠️ Technologies Used

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python         | Application and data processing |
| Apache Airflow | Workflow orchestration          |
| Docker         | Containerized environment       |
| Docker Compose | Multi-container management      |
| MongoDB        | Policy metadata storage         |
| Requests       | HTTP requests                   |
| BeautifulSoup  | Web scraping                    |
| PyPDF          | PDF text extraction             |
| python-dotenv  | Environment configuration       |

---

## 📂 Project Structure

```text
cabinet-scraper-airflow/
│
├── app/
│   ├── config.py
│   ├── database.py
│   ├── scraper.py
│   ├── pdf_downloader.py
│   └── pdf_processor.py
│
├── dags/
│   └── cabinet_scraper_dag.py
│
├── data/
│   ├── pdfs/
│   └── markdown/
│
├── logs/
│
├── config/
│
├── plugins/
│
├── .env
├── .gitignore
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

---

## 🔄 Pipeline Workflow

### 1. Scrape Policies

The scraper accesses the Cabinet Division's policies page and collects policy metadata.

Example:

```text
{
    "sr_no": "1",
    "title": "Code of Conduct for Ministers",
    "date": "June 01, 2022",
    "detail_url": "...",
    "pdf_url": "..."
}
```

The metadata is stored in MongoDB.

---

### 2. Download PDFs

The PDF downloader reads the PDF URLs stored in MongoDB and downloads the corresponding documents.

Downloaded files are stored in:

```text
data/pdfs/
```

For example:

```text
data/pdfs/
├── code_of_conduct_for_ministers.pdf
├── national_flag_of_the_federation_of_pakistan.pdf
├── awards_policy_and_guidelines-2024.pdf
└── ...
```

---

### 3. Process PDFs

The PDF processor uses `pypdf` to extract machine-readable text from downloaded PDFs.

The extracted text is converted into Markdown files:

```text
data/markdown/
```

Example:

```text
data/markdown/
├── code_of_conduct_for_ministers.md
├── awards_policy_and_guidelines-2024.md
├── civil_awards_policybooklet.md
└── ...
```

> Note: PDFs containing only scanned images may not produce Markdown because the current pipeline does not use OCR.

---

## ☁️ MongoDB

MongoDB stores the policy metadata and processing information.

Example document:

```json
{
    "sr_no": "1",
    "title": "Code of Conduct for Ministers",
    "date": "June 01, 2022",
    "detail_url": "https://cabinet.gov.pk/PolicyDetail/...",
    "pdf_url": "https://cabinet.gov.pk/SiteImage/Policy/...",
    "pdf_file": "/opt/airflow/pdfs/code_of_conduct_for_ministers.pdf",
    "markdown_file": "/opt/airflow/markdown/code_of_conduct_for_ministers.md"
}
```

The application uses:

```text
Database: cabinet_db
Collection: laws
```

---

## 🌀 Apache Airflow DAG

The Airflow DAG is defined in:

```text
dags/cabinet_scraper_dag.py
```

The workflow contains three tasks:

```python
scrape >> download >> process
```

### Task 1 — `scrape_policies`

Scrapes the Cabinet Division website and saves policy metadata to MongoDB.

### Task 2 — `download_pdfs`

Downloads the PDFs associated with the policies.

### Task 3 — `process_pdfs`

Extracts text from PDFs and generates Markdown files.

The dependency ensures that:

```text
Scraping
   ↓
must finish before
   ↓
PDF downloading
   ↓
must finish before
   ↓
PDF processing
```

---

## 🐳 Docker Architecture

The project uses Docker Compose to run the Airflow environment.

```text
                    Docker Compose
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   Airflow         PostgreSQL          Redis
   Scheduler       Metadata DB        Message Broker
        │
        ▼
   Airflow Worker
        │
        ├── Scraper
        ├── PDF Downloader
        └── PDF Processor
                 │
                 ▼
              MongoDB
```

The local `data` directory is mounted into the Airflow worker:

```text
data/pdfs      → /opt/airflow/pdfs
data/markdown  → /opt/airflow/markdown
```

This allows files generated inside the Docker container to remain accessible from the host machine.

---

## ⚙️ Setup

### Prerequisites

Install:

* Docker Desktop
* Git
* MongoDB

Docker Desktop should be running before starting Airflow.

---

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd cabinet-scraper-airflow
```

---

### 2. Configure Environment Variables

Create a `.env` file:

```env
AIRFLOW_UID=50000

MONGO_URI=mongodb://host.docker.internal:27017/
DATABASE_NAME=cabinet_db
COLLECTION_NAME=laws
```

---

### 3. Start Airflow

Initialize the Airflow environment:

```bash
docker compose up airflow-init
```

Then start the services:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

---

## 🌐 Airflow Web UI

Open:

```text
http://localhost:8080
```

Default credentials for the provided development configuration:

```text
Username: airflow
Password: airflow
```

From the Airflow UI, locate:

```text
cabinet_scraper_pipeline
```

and trigger the DAG manually.

---

## 🧪 Running Individual Components

The individual components can also be tested directly inside the Airflow worker.

### Test the scraper

```bash
docker compose exec airflow-worker python -c "from app.scraper import scrape_policies; p=scrape_policies(); print('Policies found:', len(p))"
```

### Download PDFs

```bash
docker compose exec airflow-worker python -c "from app.pdf_downloader import download_all_pdfs; download_all_pdfs()"
```

### Process PDFs

```bash
docker compose exec airflow-worker python -c "from app.pdf_processor import process_pdfs; process_pdfs()"
```

### Check MongoDB

```bash
docker compose exec airflow-worker python -c "from app.database import get_database; c=get_database(); print('Documents:', c.count_documents({}))"
```

---

## 📊 Current Pipeline Output

The scraper currently retrieves **27 policy records** from the Cabinet Division website.

The pipeline downloads the corresponding PDFs and processes PDFs containing machine-readable text into Markdown.

The current implementation intentionally does **not** use OCR, so scanned/image-only PDFs may be skipped during text extraction.

---

## 🔐 Environment & Security

Sensitive configuration should be stored in `.env` rather than hard-coded into Python files.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
```

Do not commit database credentials, API keys, passwords, or other secrets to GitHub.

---

## 🎯 Learning Objectives

This project demonstrates several important data engineering concepts:

* Web scraping
* Data ingestion
* MongoDB
* ETL/ELT-style processing
* File-based data pipelines
* PDF processing
* Workflow orchestration
* Airflow DAGs
* Task dependencies
* Docker containerization
* Environment variables
* Persistent Docker volumes
* Pipeline monitoring and logging

---

## 🔮 Future Improvements

Possible future improvements include:

* Add OCR support for scanned PDFs
* Add automatic scheduling instead of manual DAG execution
* Add retry mechanisms for failed downloads
* Detect newly published policies automatically
* Avoid downloading unchanged PDFs
* Add data validation
* Add logging and error reporting
* Add unit tests
* Add Docker image customization
* Add CI/CD with GitHub Actions
* Store processed documents in cloud object storage
* Add a downstream analytics/search pipeline

---

## 📜 License

This project is intended for educational and portfolio purposes.

The scraped documents and content belong to their respective source/rights holders.

---

## 👨‍💻 Author

**Leo**

Built as a data engineering project to demonstrate web scraping, MongoDB, PDF processing, Docker, and Apache Airflow workflow orchestration.

This version is **GitHub-ready** and presents the project as a proper data-engineering portfolio project rather than just a scraper.
