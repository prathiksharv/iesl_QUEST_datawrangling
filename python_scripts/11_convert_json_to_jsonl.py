import json

# Load the JSON file
with open('doc_extractions/Run3_Quest_Filter_Queries_Extracted.json') as f:
    data = json.load(f)

# Convert to JSONL and save
with open('Run3_Quest_Filter_Queries_Extracted_jsonl.jsonl', 'w') as f:
    for key, value in data.items():
        # Create a dictionary for each key-value pair
        record = {key: value}
        # Write the dictionary as a single JSON line
        f.write(json.dumps(record) + '\n')

print("Data successfully converted and saved!")
