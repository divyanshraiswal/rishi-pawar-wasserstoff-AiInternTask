import json
import requests
import io
import pdfplumber
from pymongo import MongoClient
from keybert import KeyBERT
import spacy
import concurrent.futures
import logging
import certifi  

# Setup logging for error handling
logging.basicConfig(
    filename='pdf_processing.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize models
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

# MongoDB Connection Setup
def get_mongo_collection(uri, db_name, collection_name):
    client = MongoClient(uri)
    return client[db_name][collection_name]

# Function to download and extract text from PDF
def download_and_extract_text(pdf_name, pdf_url):
    try:
        # Use certifi to specify the CA bundle for SSL verification
        response = requests.get(pdf_url, verify=certifi.where())  
        response.raise_for_status()
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            return ''.join(page.extract_text() or '' for page in pdf.pages)
    except Exception as e:
        logging.error(f"Error with {pdf_name}: {e}")
        return None

# Function to extract keywords
def extract_keywords(text, num_keywords=5):
    keywords = kw_model.extract_keywords(text, top_n=num_keywords)
    domain_entities = [
        ent.text for ent in nlp(text).ents if ent.label_ in {"ORG", "GPE", "LAW", "PERSON", "EVENT"}
    ]
    return list(set(kw[0] for kw in keywords) | set(domain_entities))[:num_keywords]

# Function to update MongoDB with results
def update_mongodb(collection, pdf_name, pdf_url, text, summary, keywords):
    metadata = {
        "document_name": pdf_name,
        "url": pdf_url,
        "summary": summary,
        "keywords": keywords,
        "status": "processed" if text else "failed"
    }
    collection.update_one({"document_name": pdf_name}, {"$set": metadata}, upsert=True)

# Process a single PDF: download, extract, summarize, and store
def process_pdf(pdf_name, pdf_url, collection):
    text = download_and_extract_text(pdf_name, pdf_url)
    summary = (text[:100] + '...') if text else ""
    keywords = extract_keywords(text) if text else []
    update_mongodb(collection, pdf_name, pdf_url, text, summary, keywords)

# Main function for concurrent processing
def process_pdfs(json_url, mongo_uri, db_name, collection_name, max_workers=5):
    pdf_links = requests.get(json_url).json()
    collection = get_mongo_collection(mongo_uri, db_name, collection_name)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(
            lambda item: process_pdf(item[0], item[1], collection),
            pdf_links.items()
        )

# MongoDB and JSON URL details
json_url = "https://raw.githubusercontent.com/Devian158/AI-Internship-Task/main/Dataset.json"
mongo_uri = "mongodb://localhost:27017"
db_name = "l_pdf_data"
collection_name = "l_pdf_metadata"

# Execute the script
process_pdfs(json_url, mongo_uri, db_name, collection_name)
