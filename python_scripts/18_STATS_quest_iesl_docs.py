import pandas as pd
import matplotlib.pyplot as plt
import logging

# Setup logger
logging.basicConfig(filename='stats/logs/QUEST_iesl_docs_statistics.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load the dataset
file_path = 'quest/iesl/quest.jsonl'
data = pd.read_json(file_path, lines=True)

# Count the number of documents for each query
data['doc_count'] = data['docs'].apply(len)

# Calculate min, max, and average
min_docs = data['doc_count'].min()
max_docs = data['doc_count'].max()
average_docs = data['doc_count'].mean()

# Find the minimum document count that is not zero
min_non_zero_docs = data[data['doc_count'] > 0]['doc_count'].min()

# Log the statistics
logging.info("Minimum number of documents (including zero): %s", min_docs)
logging.info("Minimum number of documents (excluding zero): %s", min_non_zero_docs)
logging.info("Maximum number of documents: %s", max_docs)
logging.info("Average number of documents: %.2f", average_docs)

# Identify and log queries with 0 documents
zero_docs_queries = data[data['doc_count'] == 0]
if not zero_docs_queries.empty:
    logging.info("Queries with 0 documents:\n%s", zero_docs_queries)
else:
    logging.info("No queries with 0 documents.")

# Print results to console for verification
print("Statistics and zero-document queries have been logged.")
print(f"Minimum document count (excluding zero): {min_non_zero_docs}")

# Create a figure to hold both the bar plot and histogram
plt.figure(figsize=(10, 12))

# Bar plot for min, max, and average document counts
plt.subplot(2, 1, 1)
plt.bar(['Minimum', 'Minimum (Excluding Zero)', 'Maximum', 'Average'], [min_docs, min_non_zero_docs, max_docs, average_docs])
plt.title('Document Statistics per Query')
plt.ylabel('Number of Documents')

# Histogram to show the distribution of document counts across queries
plt.subplot(2, 1, 2)
plt.hist(data['doc_count'], bins=20, edgecolor='black')
plt.title('Distribution of Document Counts per Query')
plt.xlabel('Number of Documents')
plt.ylabel('Frequency')

# Save the figure as an image
plt.tight_layout()
plt.savefig('stats/graphs/QUEST_iesl_docs_statistics_graph.png')
print("Graphs have been saved as QUEST_iesl_docs_statistics_graph.png")
