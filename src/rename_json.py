import os
import shutil
import re

# Input and output folder paths
input_folder = r'D:\CS418-Final-Project\src\Output_OCR_Nom_Sach_001_Processed'
output_folder = r'D:\CS418-Final-Project\src\Output_OCR_Nom_Sach_001_Processed_new'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to extract the numeric part of the filename
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

# Get all image files from the input folder
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('json'))]

# Sort files based on the extracted numeric part
sorted_files = sorted(image_files, key=extract_number)

# Rename and save files in the output folder
start_page = 222  # Adjust the starting page number as needed

for index, filename in enumerate(sorted_files, start=start_page):
    old_path = os.path.join(input_folder, filename)
    new_name = f'page_{index}.json'  # Adjust extension if needed
    new_path = os.path.join(output_folder, new_name)
    
    # Copy and rename the file
    shutil.copy2(old_path, new_path)

print("Renaming completed. All files are saved in:", output_folder)
