import json

# Filenames of the JSONL files you want to combine
file1 = 'doc_extractions/Run1_Quest_Filter_Queries_Extracted_jsonl.jsonl'
file2 = 'doc_extractions/Run2_Quest_Filter_Queries_Extracted_jsonl.jsonl'
file3 = 'doc_extractions/Run3_Quest_Filter_Queries_Extracted_jsonl.jsonl'
output_file = 'Quest_Filter_Queries_Extracted_Docs.jsonl'

# List of files to combine
files = [file1, file2, file3]

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    for fname in files:
        # Open each input file
        with open(fname, 'r') as infile:
            # Read each line (each line is a JSON object in JSONL format)
            for line in infile:
                # Write the line to the output file
                outfile.write(line)

print(f'Files combined into {output_file}')