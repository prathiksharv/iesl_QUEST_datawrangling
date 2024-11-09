import json
import logging

# Set up logging configuration
logging.basicConfig(
    filename='data_cleaning_log.log', 
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Load the JSONL file
input_file = 'doc_extractions/correct_format_json_object_files/atomic_queries_utf_encoded_json_object_structure.jsonl'
output_file = 'doc_extractions/cleaned_data.jsonl'

# Initialize an empty list to hold cleaned entries
cleaned_entries = []

# Counter for processed entries
entry_count = 0

# Process the input JSONL file
with open(input_file, 'r') as f:
    for line in f:
        entry = json.loads(line)
        atomic_query = entry.get('atomic_query')
        skip_entry = False  # Flag to track if entry should be skipped
        entry_count += 1  # Increment entry count
        
        # Print status every 100 entries
        if entry_count % 100 == 0:
            print(f"{entry_count} entries processed...")

        # Check if 'page_titles' list is empty
        if not entry.get('page_titles'):
            logging.info(f"Skipped entire entry for atomic_query '{atomic_query}' - Reason: Empty 'page_titles'")
            continue
        
        # Filter 'page_titles' and 'page_contents' based on specified conditions
        filtered_titles = []
        filtered_contents = []
        for title, content in zip(entry['page_titles'], entry['page_contents']):
            if not content:
                logging.info(f"Excluded 'page_title' '{title}' for atomic_query '{atomic_query}' - Reason: Empty 'page_contents'")
                continue
            elif title.startswith("Category:"):
                logging.info(f"Excluded 'page_title' '{title}' for atomic_query '{atomic_query}' - Reason: 'page_title' starts with 'Category:'")
                continue
            # Clean the content by removing newline characters
            clean_content = content.replace("\n", "")
            filtered_titles.append(title)
            filtered_contents.append(clean_content)
        
        # Update entry with filtered lists or log if entry is empty after filtering
        if filtered_titles and filtered_contents:
            entry['page_titles'] = filtered_titles
            entry['page_contents'] = filtered_contents
            cleaned_entries.append(entry)
        else:
            logging.info(f"Skipped entire entry for atomic_query '{atomic_query}' - Reason: No valid 'page_titles' or 'page_contents' after filtering")

# Write cleaned entries to a new JSONL file
with open(output_file, 'w') as f:
    for entry in cleaned_entries:
        json.dump(entry, f)
        f.write('\n')

print("Data cleaning complete. Cleaned data saved to", output_file)
print("Exclusion log created: 'exclusion_log.log'")
