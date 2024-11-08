import json
import logging

# Set up logging
logging.basicConfig(filename="merge_json.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Paths to your JSON files
file_paths = [
    "doc_extractions/Run1_Quest_Filter_Queries_Extracted.json",
    "doc_extractions/Run2_Quest_Filter_Queries_Extracted.json",
    "doc_extractions/Run3_Quest_Filter_Queries_Extracted.json"
]

# Initialize an empty dictionary to store merged data
merged_data = {}

try:
    key_count = 0  # Counter to track the number of keys processed

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Update merged_data with the contents of the current file
            merged_data.update(data)
            logging.info(f"Loaded data from {file_path} with {len(data)} keys.")

except Exception as e:
    logging.error(f"Error reading file {file_path}: {e}")

# Perform UTF-8 encoding on all keys and values
def utf8_encode(data):
    global key_count
    if isinstance(data, dict):
        processed_data = {}
        for key, value in data.items():
            processed_data[utf8_encode(key)] = utf8_encode(value)
            key_count += 1
            if key_count % 100 == 0:
                print(f"Processed {key_count} keys...")
                logging.info(f"Processed {key_count} keys so far.")
        return processed_data
    elif isinstance(data, list):
        return [utf8_encode(element) for element in data]
    elif isinstance(data, str):
        return data.encode("utf-8").decode("utf-8")
    else:
        return data

try:
    encoded_data = utf8_encode(merged_data)
except Exception as e:
    logging.error(f"Error during UTF-8 encoding: {e}")

# Write the merged data to a new JSON file
output_path = "doc_extractions/Quest_Filter_Queries_Extracted_JSON_utfencoded.json"
try:
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(encoded_data, outfile, ensure_ascii=False, indent=4)
    logging.info(f"Merged JSON saved at: {output_path}")
    print(f"Merged JSON saved at: {output_path}")
except Exception as e:
    logging.error(f"Error writing to file {output_path}: {e}")

