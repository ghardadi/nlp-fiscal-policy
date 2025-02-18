# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:52:30 2024

@author: wb582890
"""

import random
import numpy as np
import pandas as pd
import requests
import os
import shutil

DRM_files = pd.read_excel("PER Repository.xlsx", sheet_name="Full list")
DRM_ids = DRM_files["P number"].to_list()

# Specify the directory name
directory_name = "Public Expenditure Review1"
                
# Create the directory
try:
    os.makedirs(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

# project_id = "P075941"
# pdf_url = "http://documents.worldbank.org/curated/en/563281468204538380/pdf/761100AFR0PAD000Box377382B00PUBLIC0.pdf"

def find_keyword_in_json(data, keyword):
    """Recursively searches for a keyword in a nested JSON object."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == keyword:
                return value
            elif isinstance(value, (dict, list)):
                result = find_keyword_in_json(value, keyword)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_keyword_in_json(item, keyword)
            if result is not None:
                return result
    return None

def download_pdf(project_id, directory_name="Public Expenditure Review1"):
    url = f"https://search.worldbank.org/api/v3/wds?projectid={project_id}&lang=English&docty=Public%20Expenditure%20Review&format=json"
    
    response = requests.get(url)

    if response.status_code == 200:
        documents = response.json()
            
    # Parsing JSON data using recursion
    pdf_url = find_keyword_in_json(documents, "pdfurl")
    
    try:
        title = find_keyword_in_json(documents, "display_title")
        docdt = find_keyword_in_json(documents, "docdt")
        
        title = title.split(" : ")[0]
        title = title.split("\n")[0]
        project_name = f"{project_id} {title[:120]} {docdt[:10]}"
        
        # Send a GET request to the URL
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes

        # Open a local file with the specified filename
        filename = f"{directory_name}\\{project_name}.pdf"
        with open(filename, "wb") as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)  # Write each chunk to the file

        print(f"PDF downloaded successfully and saved as '{filename}'")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")

# download_pdf(pdf_url, project_id)

project_data = pd.DataFrame()
# keywords = ["projn", "docdt"]

for project_id in DRM_ids:
    url = f"https://search.worldbank.org/api/v3/wds?projectid={project_id}&lang=English&docty=Public%20Expenditure%20Review&format=json"
    response = requests.get(url)

    if response.status_code == 200:
        documents = response.json()
            
    # Parsing JSON data using recursion
    pdf_url = find_keyword_in_json(documents, "pdfurl")
        
    if pdf_url != None:
        # project_data = pd.concat([project_data, temp_data])
        try:
            download_pdf(project_id, directory_name)
        except:
            print(f"Error saving PDF: Program Document {project_id}")
    else:
        print(f"Program Document {project_id} not available")

def count_files(directory):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

random.seed(582890)

project_id_loc = random.sample(range(count_files(directory_name)), 20)
DRM_samples = [os.listdir(directory_name)[i] for i in project_id_loc]

sample_directory = "PER Samples"

try:
    os.makedirs(sample_directory)
    print(f"Directory '{sample_directory}' created successfully.")
except FileExistsError:
    print(f"Directory '{sample_directory}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

for i in DRM_samples:
    shutil.copy(f'{directory_name}\\{i}', f'{sample_directory}\\{i}')
    