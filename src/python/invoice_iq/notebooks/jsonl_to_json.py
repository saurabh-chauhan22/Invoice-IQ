import zipfile
import json
import random
import os

# Define the path to the ZIP file with the correct filename
zip_file_path = r'H:\testing\labeled_data\b2c160e6-fea1-4d47-982b-5e70f9971c8d.zip'

# Check if the ZIP file exists
if not os.path.exists(zip_file_path):
    print(f"Error: The file '{zip_file_path}' does not exist.")
    exit()

# Define the extraction directory (where the files will be extracted)
extraction_dir = r'H:\testing\extracted_data'  # Directory to extract the files

# Ensure the extraction directory exists
os.makedirs(extraction_dir, exist_ok=True)

# Extract the contents of the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_dir)  # Extract all files into the extraction directory

# List the files that were extracted (for verification)
extracted_files = os.listdir(extraction_dir)
print(f"Extracted files: {extracted_files}")

# Assuming the file is named 'all.jsonl', if there are multiple files, adjust accordingly
jsonl_file_path = os.path.join(extraction_dir, 'all.jsonl')

# Read the JSONL data (one line at a time)
data = []
with open(jsonl_file_path, 'r') as f:
    for line in f:
        data.append(json.loads(line))  # Parse each line as a separate JSON object

# Shuffle the data randomly
random.shuffle(data)

# Define the split ratio (e.g., 80% training, 20% testing)
split_ratio = 0.8
train_size = int(len(data) * split_ratio)

# Split the data into training and testing sets
train_data = data[:train_size]
test_data = data[train_size:]

# Paths for saving the training and testing data
train_data_path = r'H:\testing\training\train_data.json'
test_data_path = r'H:\testing\testing\test_data.json'

# Create directories for the training and testing data if they don't exist
os.makedirs(os.path.dirname(train_data_path), exist_ok=True)
os.makedirs(os.path.dirname(test_data_path), exist_ok=True)

# Save the training and testing datasets to their respective directories
with open(train_data_path, 'w') as f:
    json.dump(train_data, f, indent=4)

with open(test_data_path, 'w') as f:
    json.dump(test_data, f, indent=4)

# Print success message and data sizes
print(f"Training data saved to: {train_data_path}")
print(f"Testing data saved to: {test_data_path}")
print(f"Training data size: {len(train_data)}")
print(f"Testing data size: {len(test_data)}")
