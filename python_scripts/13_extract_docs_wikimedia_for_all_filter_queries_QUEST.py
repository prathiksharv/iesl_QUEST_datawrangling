import json
import requests
from datetime import datetime
import logging
import os

# Set up logging
logging.basicConfig(filename="error_log_3.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Record script start time
start_time = datetime.now()
print("Script start time:", start_time)

# Function to get all keys from JSON data
def get_all_keys(json_data):
    original_keys = []
    manipulated_keys = []
    
    def extract_keys(data):
        if isinstance(data, dict):
            for key, value in data.items():
                original_keys.append(key)
                manipulated_keys.append(key.replace(" ", "_"))
        elif isinstance(data, list):
            for item in data:
                extract_keys(item)
    
    extract_keys(json_data)
    return original_keys, manipulated_keys

# Load JSON data from a file
with open("preprocessed_files/iesl_quest_all_marks.json", "r") as file:
    data = json.load(file)

# Get both original and manipulated keys
original_keys, manipulated_keys = get_all_keys(data)
print("Length of all filter queries from QUEST:", len(manipulated_keys))

# Define categories range
# category_list = manipulated_keys[:1500]
# category_list = manipulated_keys[1500:3000]
category_list = manipulated_keys[3000:]

# Define the API URL for Wikimedia
url = "https://en.wikipedia.org/w/api.php"

# Initialize or load existing data
output_file_path = "Run2_Quest_Filter_Queries_Extracted.json"
if os.path.exists(output_file_path):
    with open(output_file_path, "r") as file:
        all_categories_data = json.load(file)
else:
    all_categories_data = {}

# Define a function to fetch content for a specific page
def fetch_page_content(page_id):
    content_params = {
        "action": "query",
        "pageids": page_id,
        "prop": "extracts",
        "explaintext": True,
        "format": "json"
    }
    content_response = requests.get(url, params=content_params)
    content_data = content_response.json()
    
    page_info = content_data["query"]["pages"][str(page_id)]
    return page_info.get("extract", "No content found")

# Iterate over each category in the list
for i, category_name in enumerate(category_list, start=1):
    if category_name in all_categories_data:
        # Skip if already processed
        continue
    
    try:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category_name}",
            "cmlimit": 100,
            "format": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        page_titles = []
        page_contents = []

        for page in data['query']['categorymembers']:
            page_title = page['title']
            page_id = page['pageid']
            
            page_titles.append(page_title)
            page_content = fetch_page_content(page_id)
            page_contents.append(page_content)

        all_categories_data[category_name] = {
            "page_titles": page_titles,
            "page_contents": page_contents
        }

        # Save progress every 100 queries
        if i % 100 == 0:
            with open(output_file_path, "w") as json_file:
                json.dump(all_categories_data, json_file, indent=4)
            print(f"Progress saved at {i} categories processed.")

        # Print progress every 100 queries
        if i % 100 == 0:
            print(f"Documents extracted for {i} queries")

    except Exception as e:
        logging.error(f"Error processing category '{category_name}': {e}")
        print(f"Skipping category '{category_name}' due to an error")

# Final save of data
with open(output_file_path, "w") as json_file:
    json.dump(all_categories_data, json_file, indent=4)

# Record script end time
end_time = datetime.now()
print("Script end time:", end_time)
print("Total execution time:", end_time - start_time)
