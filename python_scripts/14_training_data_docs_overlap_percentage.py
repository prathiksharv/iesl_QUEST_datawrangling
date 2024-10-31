import json
from collections import defaultdict

# Load JSON data from a file
with open('preprocessed_files/training_data.json', 'r', encoding='utf-8') as file:
    all_categories_data = json.load(file)

# Initialize a dictionary to store each document's occurrences across categories
document_queries = defaultdict(set)

# Helper function to flatten lists
def flatten(docs):
    flat_docs = []
    for doc in docs:
        if isinstance(doc, list):
            flat_docs.extend(doc)  # Extend if the item is a list
        else:
            flat_docs.append(doc)
    return flat_docs

# Map each document to the categories it appears in
for category, data in all_categories_data.items():
    docs = flatten(data.get("docs", []))  # Flatten the list of docs if needed
    for doc in docs:
        document_queries[doc].add(category)

# Prepare the output content
output_lines = []

# Calculate the overlap for each category and prepare lines for the output file
total_percentage_shared = 0
category_count = 0

for category, data in all_categories_data.items():
    category_count += 1
    docs = flatten(data.get("docs", []))  # Flatten the list of docs if needed
    shared_count = 0
    overlap_docs = []
    overlap_queries = defaultdict(list)
    
    # Count how many documents are shared with other categories
    for doc in docs:
        if len(document_queries[doc]) > 1:  # Document appears in more than one category
            shared_count += 1
            overlap_docs.append(doc)
            overlap_queries[doc] = list(document_queries[doc] - {category})  # Exclude the current category
    
    # Calculate the percentage of shared documents for this category
    if docs:
        shared_percentage = (shared_count / len(docs)) * 100
    else:
        shared_percentage = 0
    
    total_percentage_shared += shared_percentage
    
    # Append the category details to output
    output_lines.append(
        f"Category: {category}\n"
        f"Docs: {docs}\n"
        f"Overlap Docs: {overlap_docs}\n"
        f"Percentage Overlap: {shared_percentage:.2f}%\n"
        f"Overlap Queries: {overlap_queries}\n\n"
    )

    # Print status update every 5 categories
    if category_count % 5 == 0:
        print(f"Processed {category_count} categories...")

# Calculate the average shared percentage across all categories
average_shared_percentage = total_percentage_shared / len(all_categories_data)
output_lines.append(f"Average percentage of documents shared by other categories: {average_shared_percentage:.2f}%\n")

# Write the results to a text file
with open('training_data_docs_overlap_percentage.txt', 'w', encoding='utf-8') as output_file:
    output_file.writelines(output_lines)

print("Statistics written to output_stats.txt")
