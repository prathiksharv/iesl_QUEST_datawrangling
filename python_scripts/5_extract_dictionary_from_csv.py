import json

# Input and output file paths
input_file_path = 'quest/all_categories_filtered.csv'
output_file_path = 'preprocessed_files/all_categories_filtered.json'

# Dictionary to hold the JSON data
category_dict = {}

# Read and parse the CSV file
with open(input_file_path, 'r') as file:
    for line in file:
        # Split by comma to separate category and films
        category, values_str = line.strip().split(',', 1)
        
        # Replace underscores with spaces in the category label
        category = category.replace("Category:", "").replace('_', ' ').strip()
        
        
        # Split the values by the pipe symbol
        values = values_str.split('|')
        
        # Add to the dictionary with the processed category as the key
        category_dict[category] = values

# Write the dictionary to a JSON file
with open(output_file_path, 'w') as json_file:
    json.dump(category_dict, json_file, indent=4)

print(f"JSON output saved to {output_file_path}")
