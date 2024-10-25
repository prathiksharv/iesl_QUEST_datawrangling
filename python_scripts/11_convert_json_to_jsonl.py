import json

# Load the JSON file
with open('preprocessed_files/training_data.json') as f:
    data = json.load(f)

# Convert to JSONL and save
with open('preprocessed_files/training_data_jsonl.jsonl', 'w') as f:
    for key, value in data.items():
        # Create a dictionary for each key-value pair
        record = {key: value}
        # Write the dictionary as a single JSON line
        f.write(json.dumps(record) + '\n')

print("Data successfully converted and saved to 'preprocessed_files/training_data.jsonl'.")
