import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'quest/iesl/quest.jsonl'
data = pd.read_json(file_path, lines=True)

# Count the number of documents for each query
data['doc_count'] = data['docs'].apply(len)

# Calculate min, max, and average
min_docs = data['doc_count'].min()
max_docs = data['doc_count'].max()
average_docs = data['doc_count'].mean()

# Print the results
print("Minimum number of documents:", min_docs)
print("Maximum number of documents:", max_docs)
print("Average number of documents:", average_docs)

# Bar plot for min, max, and average document counts
plt.figure(figsize=(8, 5))
plt.bar(['Minimum', 'Maximum', 'Average'], [min_docs, max_docs, average_docs])
plt.title('Document Statistics per Query')
plt.ylabel('Number of Documents')
plt.show()

# Histogram to show the distribution of document counts across queries
plt.figure(figsize=(10, 6))
plt.hist(data['doc_count'], bins=20, edgecolor='black')
plt.title('Distribution of Document Counts per Query')
plt.xlabel('Number of Documents')
plt.ylabel('Frequency')
plt.show()
