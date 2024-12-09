import requests
import zipfile
import os
import json
import sys
import argparse
import shutil
from io import BytesIO

URL = "http://192.168.64.25:8142/fit"  # Replace with the real URL
FUNCTION = rf"Mz[-1.5<1.5](t,a,b,c=1[0.5<1],T11[0<4],T12[0<4]) = a \+ b*c*exp(-t/T11) \+ b*(1-c)*exp(-t/T12)"
PARAMS = {"download": "zip"}

def set_url(url):
    global URL
    URL = url

def set_FUNCTION(function):
    global FUNCTION
    FUNCTION = function

def set_PARAMS(key,value):
    global PARAMS
    PARAMS[key]=value

def query(url, file_path, params, download_folder):
    try:
#        print(f"Uploading file and {params}...to {url}")
        with open(file_path, "rb") as file:
            files = {'file': file}  
            query = requests.post(url, files=files, data=params)
        

        if query.status_code != 200:
            raise Exception(f"File upload failed: {query.status_code}, {query.text}")

#        print("File uploaded successfully. Downloading the onefite ZIP file...")

        content_type = query.headers.get('Content-Type', '')
        if "application/zip" not in content_type and "application/octet-stream" not in content_type:
            raise Exception(f"The query to {URL} does not contain a ZIP file.")
        
        os.makedirs(download_folder, exist_ok=True)  

        with zipfile.ZipFile(BytesIO(query.content)) as zip_file:
            zip_path = zip_file.namelist();
 #           print(f"Extracting ZIP file to '{download_folder}'...")
            zip_file.extractall(download_folder)

        json_content = None
#        print (f"{download_folder}/{zip_path[0]}")
        for root, _, files in os.walk(f"{download_folder}/{zip_path[0]}"):
            for file in files:
                if file.endswith(".json"):
                    json_file_path = os.path.join(root, file)
#                   print(f"Found JSON file: {json_file_path}")
                    with open(json_file_path, "r", encoding="utf-8") as json_file:
                        json_content = json.load(json_file)  # Decode JSON
                    break  # Exit after finding the first JSON file

        tmp_folder = f"{zip_path[0]}"
        parts = tmp_folder.split("/")
        json_content["tmp_folder"]= f"{download_folder}/{parts[0]}"
        if json_content is None:
            raise Exception("No JSON file found in the extracted ZIP archive.")
        else:
#           print("Decoded onefite JSON file successfully.")
            return json_content



    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def fit(file_path,DOWNLOAD_FOLDER):
    json_file = query(URL, file_path, PARAMS, DOWNLOAD_FOLDER)
    
    if json_file:
        fit_results = json_file.get("fit-results")
        if fit_results is not None:
            print(fit_results)
        else:
            print("\nKey 'fit-results' not found in the JSON file.")
    else:
        print("Failed to process the request.")


    return json_file

