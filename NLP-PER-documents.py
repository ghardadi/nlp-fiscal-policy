# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:55:45 2024

@author: wb582890
"""

import re
from pypdf import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter

nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

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
    raw_text = extract_text_from_pdf(pdf_path)
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
    return list(set(policy_sentences))

# Use the function on a PDF file
pdf_path = "Public Expenditure Review\\P155716 Ukraine - Public finance review 2017-06-27.pdf"
policy_recommendations = main(pdf_path)

print("Extracted Policy Recommendations:")
for sentence in policy_recommendations:
    print(sentence)
