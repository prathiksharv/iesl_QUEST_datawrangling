import json

# Input and output file paths
input_file_path = 'preprocessed_files/all_categories_filtered_INTERSECTION_quest_og_queries.json'
output_file_path = 'preprocessed_files/unique_og_queries_with_all_component_indivdual_query_in_all_categories_filtered_csv.json'

# Dictionary to hold the final output
output_dict = {}

# Load the input JSON file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Iterate through each entry in the JSON data
for key, value in data.items():
    # Extract the original query, query, and docs fields
    original_query = value.get("original_query")
    query = value.get("query")
    docs = value.get("docs")
    
    # Use the original_query as the key in the new dictionary
    output_dict[original_query] = {
        "query": query,
        "docs": docs
    }

# Write the output dictionary to a JSON file
with open(output_file_path, 'w') as output_file:
    json.dump(output_dict, output_file, indent=4)

print(f"Processed data saved to {output_file_path}")
