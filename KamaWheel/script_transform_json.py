import json

# Load the original JSON file
with open('KamaWheel/sex_positions_urls.json', 'r') as json_file:
    original_data = json.load(json_file)

# Create a dictionary to store positions with penetration levels
positions = {
    'shallow': [],
    'middle': [],
    'deep': [],
    'without': []
}

# Iterate through the original data and reformat it
for level, urls in original_data.items():
    for url, penetration_level, name in urls:
        positions[penetration_level].append({
            'url': url,
            'level': level,
            'name': name
        })

# Write the transformed data to a new JSON file
with open('KamaWheel/transformed_sex_positions.json', 'w') as output_file:
    json.dump(positions, output_file, indent=4)

print("Transformation complete. Result saved in 'transformed_sex_positions.json'.")
