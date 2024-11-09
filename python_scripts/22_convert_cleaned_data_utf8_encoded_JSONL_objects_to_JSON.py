import json

# File paths
input_file = 'doc_extractions/cleaned_data/cleaned_data_utf8_encoded.jsonl'
output_file = 'doc_extractions/cleaned_data/cleaned_data_utf8_encoded_JSON.json'

# Read the JSONL file and convert to a list of JSON objects
data = []
with open(input_file, 'r', encoding='utf-8') as infile:
    for line in infile:
        # Load each line as a JSON object and append to the list
        data.append(json.loads(line))

# Write the list of JSON objects to a JSON file
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)

print("Conversion complete. JSON data saved to", output_file)
