import json
import logging

# Configure logging
logging.basicConfig(filename='processing_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the Analysis JSONL file
analysis_file_path = 'doc_extractions/Quest_Filter_Queries_Extracted_Docs_Jsonl_utfencoded.jsonl'

# Load the entire content of the Analysis.jsonl file
with open(analysis_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Try to parse the content as a JSON array
try:
    analysis_data_list = json.loads(content)
    print(f"Successfully parsed {len(analysis_data_list)} entries from Analysis.jsonl")
except json.JSONDecodeError as e:
    print("Failed to parse JSON:", e)
    analysis_data_list = []

# If no data was parsed, notify the user
if not analysis_data_list:
    print("No data was parsed from the input file. Please check the file format.")
else:
    # Transform the data
    def convert_analysis_list_to_quest_format(data_list):
        transformed_data = []
        for i, entry in enumerate(data_list, start=1):
            try:
                # Assuming each entry has one key (the atomic query)
                for key, content in entry.items():
                    transformed_entry = {
                        "atomic_query": key,
                        "page_titles": content.get("page_titles", []),
                        "page_contents": content.get("page_contents", [])
                    }
                    transformed_data.append(transformed_entry)
                
                # Print progress every 100 entries
                if i % 100 == 0:
                    print(f"Processed {i} entries...")

            except Exception as e:
                # Log skipped entries with atomic_query details
                logging.warning(f"Skipped entry with atomic_query '{key}': {e}")

        return transformed_data

    quest_format_data = convert_analysis_list_to_quest_format(analysis_data_list)

    # Save to output file
    if not quest_format_data:
        print("No transformed data to write to the output file.")
    else:
        with open('quest_formatted_output.jsonl', 'w', encoding='utf-8') as f:
            for entry in quest_format_data:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        print("Transformation complete. Data saved to 'quest_formatted_output.jsonl'")
