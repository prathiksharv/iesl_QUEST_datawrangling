import json
import logging

# Configure logging
logging.basicConfig(filename='utf-encode_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Process JSONL file
input_file = 'doc_extractions/Quest_Filter_Queries_Extracted_Docs.jsonl'
output_file = 'Quest_Filter_Queries_Extracted_Docs_Jsonl.jsonl'
# input_file = 'doc_extractions/Sample_Jsonl.jsonl'
# output_file = 'Sample_jsonl.jsonl'

def encode_utf8(data):
    """Recursively encode all string values in the dictionary to UTF-8."""
    if isinstance(data, dict):
        return {key: encode_utf8(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [encode_utf8(item) for item in data]
    elif isinstance(data, str):
        return data.encode('utf-8').decode('utf-8')
    return data

def process_jsonl(input_file, output_file):
    output_data = []
    count = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                record = json.loads(line)
                encoded_record = encode_utf8(record)
                output_data.append(encoded_record)
                count += 1

                # Save progress and print every 100 records
                if count % 100 == 0:
                    with open(output_file, 'w', encoding='utf-8') as outfile:
                        json.dump(output_data, outfile, ensure_ascii=False, indent=4)
                    logging.info(f'Saved {count} records to {output_file}')
                    print(f'{count} records processed and saved to {output_file}')

    except Exception as e:
        logging.error(f'Error at record {count}: {str(e)}')
        print(f'Error at record {count}: {str(e)}')

    # Final save after processing all records
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4)
    logging.info(f'Processing complete. Total records processed: {count}')
    print(f'Processing complete. Total records processed: {count}')

# Run the function
process_jsonl(input_file, output_file)
