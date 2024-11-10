import json
import re

# File paths
quest_file_path = 'quest/val.jsonl'
dataset = 'doc_extractions/cleaned_data/cleaned_data_utf8_encoded_jsonl_format.jsonl'  # Update with the actual path

# Step 1: Extract marked terms from 'original_query' in quest file
original_queries = set()
mark_pattern = re.compile(r"<mark>(.*?)</mark>")  # Regex pattern to extract text within <mark> tags

with open(quest_file_path, 'r') as val_file:
    for line in val_file:
        data = json.loads(line)
        original_query = data.get('original_query')
        
        # Process only if 'original_query' is not None
        if original_query:
            # Find all marked terms within 'original_query'
            marks = mark_pattern.findall(original_query)
            for mark in marks:
                # Replace spaces with underscores in each extracted mark
                processed_mark = mark.replace(" ", "_")
                original_queries.add(processed_mark)

# Step 2: Count 'atomic_query' entries in New_JSON_Object_Structure.jsonl that match modified original_queries
atomic_query_count = 0

with open(dataset, 'r') as new_json_file:
    for line in new_json_file:
        data = json.loads(line)
        atomic_query = data.get('atomic_query', "")
        
        # Replace spaces with underscores in atomic_query and check for match
        if atomic_query.replace(" ", "_") in original_queries:
            atomic_query_count += 1

# Display the result
print("Number of 'atomic_query' entries that match modified marks in 'original_query' of", quest_file_path, "file:", atomic_query_count)
