import requests
import json

# Define a list of categories to search
category_list = ["1574_books", "Flora_of_Antarctica", "meropidae"]

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
for category_name in category_list:
    # Parameters to fetch pages in the current category
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category_name}",
        "cmlimit": 10,  # Number of results to return
        "format": "json"
    }

    # Send a request to get the list of pages in the category
    response = requests.get(url, params=params)
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

# Print the resulting JSON object (for testing purposes)
print(json.dumps(all_categories_data, indent=4))

# Optionally save the result to a JSON file
with open("categories_data.json", "w") as json_file:
    json.dump(all_categories_data, json_file, indent=4)
