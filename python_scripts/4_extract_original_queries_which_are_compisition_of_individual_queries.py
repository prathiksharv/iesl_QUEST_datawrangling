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

def extract_masked_tokens(text):
    """Extract masked tokens (marked by <mark> ... </mark>) from a string."""
    pattern = r"<mark>(.*?)</mark>"
    return [token.lower() for token in re.findall(pattern, text)]

def filter_queries(quest_og_query_data, quest_individual_query_data):
    """Filter and store records from quest_og_query where all masked tokens are in quest_individual_query."""
    result = {}

    # Get individual query keys as a set
    individual_queries = set(quest_individual_query_data.keys())

    for record in quest_og_query_data:
        original_query = record.get("original_query")
        if original_query:
            # Extract all masked tokens from original_query
            masked_tokens = extract_masked_tokens(original_query)
            
            # Check if all tokens are in the individual queries
            if all(token in individual_queries for token in masked_tokens):
                # Use the original query's masked tokens as the key
                # Add to the result dictionary
                result[original_query] = {
                    "query": record.get("query"),
                    "docs": record.get("docs"),
                    "original_query": original_query
                }
                
    return result

# File paths for input and output
quest_og_query_file = 'original_queries/quest_og_query.jsonl'
quest_individual_query_file = 'mapped_queries/quest_individual_query.json'
output_file = 'analysis_og_queries_composition_of_individual_queries.json'

# Load the data from both files
quest_og_query_data = load_jsonl(quest_og_query_file)
quest_individual_query_data = load_json(quest_individual_query_file)

# Filter the queries
filtered_queries = filter_queries(quest_og_query_data, quest_individual_query_data)

# Write the result to a JSON file
with open(output_file, 'w') as outfile:
    json.dump(filtered_queries, outfile, indent=4)

print(f"Filtered queries saved to {output_file}")
