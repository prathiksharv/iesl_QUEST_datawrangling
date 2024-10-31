import json
import requests
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename="error_log_2.log", level=logging.ERROR, 
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
                original_keys.append(key)  # Store original key
                manipulated_keys.append(key.replace(" ", "_"))  # Store key with underscores
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

#########################################################################

# category_list = manipulated_keys[:1500]
category_list = manipulated_keys[1500:3000]
# category_list = manipulated_keys[3000:]


# Define the API URL for Wikimedia
url = "https://en.wikipedia.org/w/api.php"

# Initialize an empty dictionary to store the data for each category
all_categories_data = {}

# Define a function to fetch content for a specific page
def fetch_page_content(page_id):
    content_params = {
        "action": "query",
        "pageids": page_id,
        "prop": "extracts",  # Fetch the page extract (summary/content)
        "explaintext": True,  # Return plain text without HTML formatting
        "format": "json"
    }
    content_response = requests.get(url, params=content_params)
    content_data = content_response.json()
    
    # Extract and return the page content
    page_info = content_data["query"]["pages"][str(page_id)]
    return page_info.get("extract", "No content found")

# Iterate over each category in the list
for i, category_name in enumerate(category_list, start=1):
    try:
        # Parameters to fetch pages in the current category
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category_name}",
            "cmlimit": 100,  # Number of results to return
            "format": "json"
        }

        # Send a request to get the list of pages in the category
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Initialize lists to store page titles and contents for this category
        page_titles = []
        page_contents = []

        # Extract the page IDs from the response and fetch their content
        for page in data['query']['categorymembers']:
            page_title = page['title']
            page_id = page['pageid']
            
            # Append the title to the list of titles
            page_titles.append(page_title)
            
            # Fetch the content of the page and append to the list of contents
            page_content = fetch_page_content(page_id)
            page_contents.append(page_content)

        # Add the titles and contents to the dictionary for this category
        all_categories_data[category_name] = {
            "page_titles": page_titles,
            "page_contents": page_contents
        }

        # Print progress every 100 queries
        if i % 100 == 0:
            print(f"Documents extracted for {i} queries")

    except Exception as e:
        # Log the error with the problematic key
        logging.error(f"Error processing category '{category_name}': {e}")
        print(f"Skipping category '{category_name}' due to an error")

# # Print the resulting JSON object (for testing purposes)
# print(json.dumps(all_categories_data, indent=4))

# Optionally save the result to a JSON file
with open("Run2_Quest_Filter_Queries_Extracted.json", "w") as json_file:
    json.dump(all_categories_data, json_file, indent=4)
    
# Record script end time
end_time = datetime.now()
print("Script end time:", end_time)

print("Total execution time:", end_time - start_time)
