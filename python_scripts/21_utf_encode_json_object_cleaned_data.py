import json
import logging

# Set up logging for problematic lines
logging.basicConfig(
    filename='cleaned_data_utf8_encode_log.log',
    level=logging.ERROR,
    format='%(asctime)s - %(message)s'
)

# File paths
input_file = 'doc_extractions/cleaned_data/cleaned_data.jsonl'
output_file = 'doc_extractions/cleaned_data/cleaned_data_utf8_encoded.jsonl'

# Function to encode all keys and values in a dictionary to UTF-8
def utf8_encode_dict(d):
    return {key.encode('utf-8').decode('utf-8'): 
            value.encode('utf-8').decode('utf-8') if isinstance(value, str) else
            [v.encode('utf-8').decode('utf-8') for v in value] if isinstance(value, list) else value
            for key, value in d.items()}

# Initialize a counter for processed records
record_count = 0

# Read, process, and write to new JSONL file with UTF-8 encoding
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        try:
            # Attempt to load the JSON object
            entry = json.loads(line)
            
            # Encode all keys and values to UTF-8
            encoded_entry = utf8_encode_dict(entry)
            
            # Write the encoded entry to the output file in JSONL format
            json.dump(encoded_entry, outfile, ensure_ascii=False)
            outfile.write('\n')
            
            # Increment and print progress every 100 records
            record_count += 1
            if record_count % 100 == 0:
                print(f"{record_count} records processed...")
        
        except json.JSONDecodeError as e:
            # Extract atomic_query if available, log the problematic line, and skip it
            try:
                problematic_entry = json.loads(line)
                atomic_query = problematic_entry.get('atomic_query', 'Unknown')
            except json.JSONDecodeError:
                atomic_query = 'Unknown'
            
            logging.error(f"JSONDecodeError for line {record_count + 1} (atomic_query='{atomic_query}'): {e}")
            print(f"Skipping problematic line {record_count + 1} due to JSONDecodeError.")

print("UTF-8 encoding complete. Encoded data saved to", output_file)
print("Check 'error_log.log' for any problematic lines.")

