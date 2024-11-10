import json

# Initialize counters and sets for analysis
unique_page_titles = set()
total_page_titles = 0
query_count = 0

# Load the JSONL file
file_path = 'doc_extractions/cleaned_data/cleaned_data_utf8_encoded_jsonl_format.jsonl'

with open(file_path, 'r') as file:
    for line in file:
        # Parse each JSON object
        data = json.loads(line)
        
        # Extract 'page_titles' for each query
        page_titles = data.get('page_titles', [])
        
        # Add page titles to the set of unique titles
        unique_page_titles.update(page_titles)
        
        # Update counters for average calculation
        total_page_titles += len(page_titles)
        query_count += 1
        
        # Print progress every 100 records
        if query_count % 100 == 0:
            print(f"{query_count} records processed...")

# Calculate total unique page titles and average page titles per query
total_unique_page_titles = len(unique_page_titles)
average_page_titles_per_query = total_page_titles / query_count if query_count else 0

# Display results
print("Total unique 'page_titles':", total_unique_page_titles)
print("Average 'page_titles' per query:", average_page_titles_per_query)
