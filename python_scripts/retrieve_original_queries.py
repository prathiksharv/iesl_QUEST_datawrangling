import json

def filter_and_write_non_null_original_query(input_file_path, output_file_path):
    # Open the input and output files
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        # Read each line in the input JSONL file
        for line in infile:
            # Parse the JSON line
            data = json.loads(line)
            
            # Check if 'original_query' is not null
            if data.get("original_query") is not None:
                # Write the line to the output JSONL file
                json.dump(data, outfile)
                outfile.write('\n')  # Write a newline after each JSON object

# Input file path and output file path
input_file_path = 'test.jsonl'
output_file_path = 'original_queries/test_og_query.jsonl'

# Filter and write examples with non-null 'original_query' to a new file
filter_and_write_non_null_original_query(input_file_path, output_file_path)

print(f"Filtered examples written to {output_file_path}")
