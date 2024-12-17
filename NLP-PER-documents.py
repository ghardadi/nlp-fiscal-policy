# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:55:45 2024

@author: wb582890
"""

# import pandas as pd 
# import spacy 
# import requests 
# from bs4 import BeautifulSoup
# nlp = spacy.load("en_core_web_sm")
# pd.set_option("display.max_rows", 200)

import re
# from pypdf import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter
import pdfplumber
# import fitz  # PyMuPDF

nltk.download('punkt')

# def extract_text_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# def extract_clean_text(file_path):
#     reader = PdfReader(file_path)
#     text = ""
#     for page in reader.pages:
#         # Replace newlines and extra spaces
#         text += page.extract_text().replace("\n", " ").strip()
#     return " ".join(text.split())  # Remove multiple spaces

def extract_clean_text(file_path):
    text = ""
    tables_from_pdf = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Extract tables
            tables = page.extract_tables()
            if tables:  # Collect tables if they exist
                tables_from_pdf.extend(tables)
            
            # Extract text, even if tables are present
            page_text = page.extract_text()
            if page_text:  # Check for NoneType
                text += " ".join(page_text.split()).strip() + " "  # Clean up extra spaces
    
    # Return the text (without table contents) and all tables
    return text.strip(), tables_from_pdf

pdf_path = "Public Expenditure Review\\P174959 Angola - Public Finance Review 2023-02-28.pdf"
text, tables = extract_clean_text(pdf_path)

# def extract_clean_text(file_path):
#     doc = fitz.open(file_path)
#     text = ""
#     for page in doc:
#         text += page.get_text().replace("\n", " ").strip()
#     return " ".join(text.split())  # Remove multiple spaces

def clean_and_tokenize(text):
    # Split text into sentences
    sentences = sent_tokenize(text)
    return sentences

def is_policy_recommendation(sentence):
    # Define patterns for imperative verbs and keywords
    imperative_verbs = r"\b(should|must|recommend|advise|encourage|propose|require)\b"
    if re.search(imperative_verbs, sentence, re.IGNORECASE):
        return True
    return False

def extract_from_bullets_or_tables(text):
    # Look for bullet points (e.g., "-", "*") and table-like structures
    bullets_and_tables = re.findall(r"[-*•]\s.*", text)
    return bullets_and_tables

def extract_repeated_sentences(sentences):
    # Count sentence repetitions
    sentence_counts = Counter(sentences)
    repeated_sentences = [sentence for sentence, count in sentence_counts.items() if count > 1]
    return repeated_sentences

def main(pdf_path):
    # Extract and process text
    raw_text = extract_clean_text(pdf_path)
    sentences = clean_and_tokenize(raw_text)
    
    # Filter sentences with policy-like characteristics
    policy_sentences = [s for s in sentences if is_policy_recommendation(s)]
    
    # Extract sentences from bullets or tables
    bullets_or_table_sentences = extract_from_bullets_or_tables(raw_text)
    policy_sentences.extend(bullets_or_table_sentences)
    
    # Find repeated sentences
    repeated_sentences = extract_repeated_sentences(sentences)
    policy_sentences.extend(repeated_sentences)
    
    # Remove duplicates and return results
    return list(set(policy_sentences)), sentences

# Use the function on a PDF file
policy_recommendations, sentences = main(pdf_path)

print("Extracted Policy Recommendations:")
for sentence in policy_recommendations:
    print(sentence)

