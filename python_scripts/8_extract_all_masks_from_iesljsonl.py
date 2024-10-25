import json
import re

def extract_single_masked_token(input_file_path, output_file_path):
    # Regular expression pattern to find <mark> ... </mark> tags
    mask_pattern = r"<mark>(.*?)</mark>"
    
    # Dictionary to hold the result
    masked_token_dict = {}

    # Open the input file
    with open(input_file_path, 'r') as infile:
        for line in infile:
            # Parse the JSON line
            data = json.loads(line)

            # Ensure 'original_query' and 'query' are present and not null
            original_query = data.get("original_query")
            query = data.get("query")
            if original_query and query:
                # Find all masked tokens within <mark> ... </mark>
                masked_tokens = re.findall(mask_pattern, original_query)

                # Get the relevant docs
                relevant_docs = data.get("docs", [])
                
                # Loop through all masked tokens and process each one
                for masked_token in masked_tokens:
                    # DO NOT Convert the masked token to lowercase as wkipedia search is case sensitive
                    masked_key = masked_token

                    # Check if the masked_key already exists in the dictionary
                    if masked_key in masked_token_dict:
                        # Append to the existing list of original queries, docs, and queries
                        masked_token_dict[masked_key]["original_query"].append(original_query)
                        masked_token_dict[masked_key]["query"].append(query)
                        masked_token_dict[masked_key]["docs"].append(relevant_docs)
                    else:
                        # Create a new entry with the original query, docs, and query as lists
                        masked_token_dict[masked_key] = {
                            "original_query": [original_query],
                            "query": [query],
                             "docs": [relevant_docs],
                        }

    # Write the dictionary to a JSON file
    with open(output_file_path, 'w') as outfile:
        json.dump(masked_token_dict, outfile, indent=4)

# Input and output file paths
input_file_path = 'quest/iesl/quest.jsonl'
output_file_path = 'preprocessed_files/iesl_quest_all_marks.json'

# Run the function to extract and save the data
extract_single_masked_token(input_file_path, output_file_path)

print(f"Output saved to {output_file_path}")
