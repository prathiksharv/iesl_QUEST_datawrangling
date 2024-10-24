import json

def load_json(file_path):
    """Load the JSON data from the given file path."""
    with open(file_path, 'r') as file:
        return json.load(file)

def find_overlapping_and_non_overlapping_keys(quest_data, category_data):
    # Extract keys from both dictionaries and convert them to lowercase
    quest_keys = {key.lower() for key in quest_data.keys()}
    category_keys = {key.lower() for key in category_data.keys()}
    
    # Find keys present in both dictionaries
    overlapping_keys = quest_keys.intersection(category_keys)
    
    # Find keys present in iesl_quest_all_marks but not in all_categories_filtered
    quest_non_overlapping = quest_keys.difference(category_keys)
    
    return overlapping_keys, quest_non_overlapping

def main():
    # Load the JSON data from both files
    quest_data = load_json('preprocessed_files/iesl_quest_all_marks.json')
    category_data = load_json('preprocessed_files/all_categories_filtered.json')
    
    # Find overlapping and non-overlapping keys
    overlapping_keys, quest_non_overlapping = find_overlapping_and_non_overlapping_keys(quest_data, category_data)
    
    # Print the results
    print(f"Keys present in both iesl_quest_all_marks and all_categories_filtered: {len(overlapping_keys)}")
    print(f"Keys present in iesl_quest_all_marks but NOT in all_categories_filtered: {len(quest_non_overlapping)}")
    
    # # Print the lists of keys
    # print("\nKeys present in both iesl_quest_all_marks and all_categories_filtered:")
    # print(overlapping_keys)
    
    # print("\nKeys present in iesl_quest_all_marks but NOT in all_categories_filtered:")
    # print(quest_non_overlapping)

if __name__ == "__main__":
    main()
