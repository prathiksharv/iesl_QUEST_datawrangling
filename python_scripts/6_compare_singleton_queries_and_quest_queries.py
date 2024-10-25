#script to extract all queries from quest_og_original.jsonl such that all lower(<marks>) within "original_query" of each record is present as a lower(key) in all_categories_filtered.json
#extract such queries and add them to dictionary in this format: <mark> value acting as key and having two values in a list "original query" of the <mark> and "docs"

import json
import re

def load_jsonl(file_path):
    """Load a JSONL file into a list of dictionaries."""
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def load_json(file_path):
    """Load a JSON file into a dictionary."""
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_marked_tokens(text):
    """Extract all <mark>...</mark> tokens from a string and DO NOT convert to lowercase as wikipedia search by category is case sensitive."""
    pattern = r"<mark>(.*?)</mark>"
    return [token for token in re.findall(pattern, text)]

def filter_queries(quest_data, category_data):
    """Filter and extract records where all <mark> tokens are in category_data keys."""
    result = {}

    # DO NOT convert category keys to lowercase for comparison as wikipedia search by category is case sensitive
    category_keys = {key for key in category_data.keys()}

    for record in quest_data:
        original_query = record.get("original_query")
        if original_query:
            # Extract <mark> tokens from the original_query
            marked_tokens = extract_marked_tokens(original_query)
            
            # Check if all marked tokens are present in the category keys
            if all(token in category_keys for token in marked_tokens):
                for token in marked_tokens:
                    # Add to result with each <mark> token as a key
                    result[token] = {
                        "original_query": original_query,
                        "query": record.get("query"),
                        "docs": record.get("docs")
                    }

    return result

# Input and output file paths
quest_file_path = 'original_queries/quest_og_query.jsonl'
category_file_path = 'preprocessed_files/all_categories_filtered.json'
output_file_path = 'all_categories_filtered_INTERSECTION_quest_og_queries.json'

# Load the data from both files
quest_data = load_jsonl(quest_file_path)
category_data = load_json(category_file_path)

# Filter and extract the relevant queries
filtered_queries = filter_queries(quest_data, category_data)

# Write the result to a JSON file
with open(output_file_path, 'w') as output_file:
    json.dump(filtered_queries, output_file, indent=4)

print(f"Filtered queries saved to {output_file_path}")
