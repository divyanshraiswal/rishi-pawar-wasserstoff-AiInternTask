# PDF Processing and Metadata Extraction

This project is designed to automate the download, text extraction, summarization, and keyword extraction of PDF files, with results stored in a MongoDB database. It uses `pdfplumber` for extracting text from PDFs and `KeyBERT` for keyword extraction, along with `spacy` for domain-specific entity recognition. The process is handled concurrently using `concurrent.futures`.

## Features

- **Download PDFs** from a provided JSON file containing links.
- **Extract text** from PDFs using `pdfplumber`.
- **Summarize content** and **extract keywords** using `KeyBERT` and `spacy`.
- Store results in **MongoDB**, including document metadata and processing status.
- **Concurrent processing** for improved performance.

## Prerequisites

- **Docker** installed on your system.
- A running instance of **MongoDB** or a MongoDB URI if using a cloud database.
- A JSON file with PDF URLs, structured as `{ "pdf_name": "pdf_url" }`.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pdf-processing-app.git
   cd pdf-processing-app
   
2. **Build the Docker image**:
   ```bash
   docker build -t pdf-processing-app

3. **Run the Docker container**
   ```bash
   docker run -e MONGO_URI="mongodb://host:port" \
           -e DB_NAME="l_pdf_data" \
           -e COLLECTION_NAME="l_pdf_metadata" \
           -p 27017:27017 pdf-processing-app



## Overview of `app.py`

The `app.py` file is responsible for downloading PDFs, extracting text, summarizing content, extracting keywords, and storing metadata in MongoDB. Here’s a breakdown of the key components:

| **Component**             | **Description**                                                                                               |
|---------------------------|---------------------------------------------------------------------------------------------------------------|
| **Imports**               | Uses `requests` for downloading PDFs, `pdfplumber` for text extraction, `pymongo` for MongoDB interactions, `KeyBERT` for keyword extraction, and `spacy` for entity recognition. |
| **Model Initialization**  | Initializes `spacy` for NLP tasks and `KeyBERT` for keyword extraction.                                        |
| **MongoDB Connection**    | Connects to a MongoDB database using a URI and returns the specified collection for storing metadata.          |
| **Download and Extract Text** | Downloads PDFs and extracts text using `pdfplumber`. Handles errors with logging.                              |
| **Keyword Extraction**    | Extracts top keywords using `KeyBERT` and identifies domain-specific entities using `spacy`.                   |
| **Update MongoDB**        | Updates the MongoDB collection with extracted metadata, including the document name, URL, summary, keywords, and status. |
| **Process Single PDF**    | Downloads, extracts text, summarizes, and stores metadata for a single PDF.                                    |
| **Concurrent Processing** | Uses `ThreadPoolExecutor` to process multiple PDFs concurrently, improving efficiency.                         |
| **Execution**             | Runs the processing function with user-specified MongoDB details and a JSON URL of PDF links.                  |
