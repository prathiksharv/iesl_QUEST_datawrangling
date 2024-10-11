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

            # Ensure 'original_query' is present and not null
            original_query = data.get("original_query")
            if original_query:
                # Find all masked tokens within <mark> ... </mark>
                masked_tokens = re.findall(mask_pattern, original_query)
                
                # Check if there is only one masked token
                if len(masked_tokens) == 1:
                    # Extract the token and convert it to lowercase
                    masked_key = masked_tokens[0].lower()
                    
                    # Get the relevant docs
                    relevant_docs = data.get("docs", [])
                    
                    # Create an entry in the dictionary
                    masked_token_dict[masked_key] = {
                        "original_query": original_query,
                        "docs": relevant_docs
                    }

    # Write the dictionary to a JSON file
    with open(output_file_path, 'w') as outfile:
        json.dump(masked_token_dict, outfile, indent=4)

# Input and output file paths
input_file_path = 'quest/iesl/quest.jsonl'
output_file_path = 'mapped_queries/quest_mapped_query.json'

# Run the function to extract and save the data
extract_single_masked_token(input_file_path, output_file_path)

print(f"Output saved to {output_file_path}")
