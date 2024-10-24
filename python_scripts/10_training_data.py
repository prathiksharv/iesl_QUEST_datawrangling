import json

# Load the JSON files
with open('preprocessed_files/all_categories_filtered_INTERSECTION_quest_og_queries.json') as f:
    queries_data = json.load(f)

with open('preprocessed_files/all_categories_filtered.json') as f:
    categories_data = json.load(f)

# Function to normalize document titles (replace "_" with "") and convert to lower case
def normalize_title(title):
    return title.replace("_", " ").lower()

# Load the documents.jsonl file (line-separated JSON)
documents_data = []
with open('quest/documents.jsonl') as f:
    for line in f:
        documents_data.append(json.loads(line))

# Function to search for document text based on title (lower case comparison)
def get_document_text(title):
    title_lower = title.lower()
    for doc in documents_data:
        if doc['title'].lower() == title_lower:
            return doc['text']
    return None

# Create the output structure
output_data = {}

# Iterate over the keys in queries_data
for key in queries_data.keys():
    key_lower = key.lower()  # Convert the key to lowercase for case-insensitive matching
    if key_lower not in output_data:
        output_data[key_lower] = {}

    output_data[key_lower]['docs'] = []

    # Extract "docs" from matching categories in all_categories_filtered
    if key in categories_data:
        normalized_docs = [normalize_title(doc) for doc in categories_data[key]]
        output_data[key_lower]['docs'] = normalized_docs

        # Append only the document text from documents.jsonl
        output_data[key_lower]['docs_text'] = []
        for doc_title in normalized_docs:
            doc_text = get_document_text(doc_title)
            if doc_text:
                output_data[key_lower]['docs_text'].append(doc_text)  # Only append the text content
            else:
                output_data[key_lower]['docs_text'].append("Document text not found")

# Save the output to a JSON file
with open('preprocessed_files/training_data.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print("JSON data successfully generated and saved to 'preprocessed_files/training_data.json'.")
