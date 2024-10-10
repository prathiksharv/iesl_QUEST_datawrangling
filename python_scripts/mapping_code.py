import json
import re
from collections import defaultdict

def create_masked_entity_dictionary(input_file_path):
    # Regular expression pattern to extract <mark> ... </mark> tags
    mask_pattern = r"<mark>(.*?)</mark>"

    # Dictionary to hold the masked entities as keys
    masked_entity_dict = defaultdict(list)

    # Open the input file
    with open(input_file_path, 'r') as infile:
        for line in infile:
            # Parse each JSON line
            data = json.loads(line)

            # Ensure 'original_query' is present and not null
            original_query = data.get("original_query")
            if original_query:
                # Find all masked entities within <mark> ... </mark>
                masked_entities = re.findall(mask_pattern, original_query)
                
                # Convert each entity to lowercase
                masked_keys = [entity.lower() for entity in masked_entities]

                # Retrieve relevant documents
                relevant_docs = data.get("docs", [])
                
                # Populate the dictionary with each masked entity
                for key in masked_keys:
                    masked_entity_dict[key].append({
                        "original_query": original_query,
                        "relevant_docs": relevant_docs
                    })

    return masked_entity_dict

# Input and output file paths
input_file_path = 'original_queries/val_og_query.jsonl'
output_file_path = 'mapped_queries/val_mapped_query.json'

# Create the dictionary
masked_entity_dict = create_masked_entity_dictionary(input_file_path)

# Write the dictionary to a JSON file
with open(output_file_path, 'w') as outfile:
    json.dump(masked_entity_dict, outfile, indent=4)

print(f"Dictionary written to {output_file_path}")
