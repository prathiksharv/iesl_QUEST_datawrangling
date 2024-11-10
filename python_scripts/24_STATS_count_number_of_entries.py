file_path = 'quest/val.jsonl'

# Initialize counter
entry_count = 0

with open(file_path, 'r') as file:
    for line in file:
        entry_count += 1

print("Total number of entries:", entry_count)
