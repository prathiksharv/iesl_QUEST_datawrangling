import json

file_path = 'quest/test.jsonl'

# Initialize counters
total_relevant_docs = 0
entry_count = 0

with open(file_path, 'r') as file:
    for line in file:
        # Parse each JSON object
        data = json.loads(line)
        
        # Extract relevant documents count
        relevant_docs = data.get('docs', [])
        
        # Update total relevant documents and entry count
        total_relevant_docs += len(relevant_docs) if isinstance(relevant_docs, list) else relevant_docs
        entry_count += 1

# Calculate average relevant documents
average_relevant_docs = total_relevant_docs / entry_count if entry_count else 0

# Display result
print("Average relevant docs across all entries:", average_relevant_docs)
