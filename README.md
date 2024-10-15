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

