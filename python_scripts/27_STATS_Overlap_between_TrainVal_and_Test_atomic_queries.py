import json

# Define function to read and process marked queries from a JSONL file
def extract_marked_queries(file_path):
    marked_queries = set()
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            # Extract the "original_query" field, defaulting to an empty string if not present
            query = data.get("original_query", "")
            if isinstance(query, str):  # Ensure query is a string before processing
                # Replace " " and "_" and add to marked queries set
                for mark in query.split():
                    mark = mark.replace(" ", "_")
                    marked_queries.add(mark)
    return marked_queries

# File paths
file1_path = 'quest/train_aug.jsonl'  # Update paths to include file2 and file3 once available
file2_path = 'quest/val.jsonl'
file3_path = 'quest/test.jsonl'

# Process each file to create marked_queries1, marked_queries2, marked_queries3
marked_queries1 = extract_marked_queries(file1_path)
marked_queries2 = extract_marked_queries(file2_path)
marked_queries3 = extract_marked_queries(file3_path)

# Combine marked_queries1 and marked_queries2
marked_queries_combined = marked_queries1.union(marked_queries2)

# Calculate overlap between marked_queries_combined and marked_queries3
overlap_queries_train_and_val = list(marked_queries1.intersection(marked_queries2))
overlap_queries = list(marked_queries_combined.intersection(marked_queries3))

# Print results
print("Marked queries in Train:", len(marked_queries1), "Marked queries in Val:", len(marked_queries2) )
print("Overlap count between train and val:", len(overlap_queries_train_and_val) )
print("Marked Queries Combined in Train and Val:", len(marked_queries_combined))
print("Marked queries in Test:", len(marked_queries3))
print("Overlap Queries between Train, Val marked queries and Test marked queries:", len(overlap_queries))