import os
from PIL import Image

# Path to the folder containing the images
input_folder = r"D:\CS418-Final-Project\extracted_imgs\Sach-Nom-Cong-Giao-1995-001"
output_folder = r"D:\CS418-Final-Project\extracted_imgs\Sach-Nom-Cong-Giao-1995-001-rotated"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):  # Supported image formats
        file_path = os.path.join(input_folder, filename)

        with Image.open(file_path) as img:
            rotated_img = img.rotate(-2, resample=Image.BICUBIC, expand=True)
            rotated_img.save(os.path.join(output_folder, filename))

print("Rotation completed!")
