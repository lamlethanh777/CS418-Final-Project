import os
import fitz
import cv2
import numpy as np
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate


# region Divide Image
def find_best_division_line(image, bias):
    if image is None:
        raise ValueError("Image data is None")

    # Correct skew
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    skew_angle = get_angle(gray)
    rotated_image = rotate(image, skew_angle)
    gray = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    # Search for the division line with the most white pixels (> 150)
    start_x = int((0.48 + bias) * width)
    end_x = int((0.52 + bias) * width)
    columns = gray[:, start_x:end_x]
    counts = np.sum(columns > 150, axis=0)
    best_line_x = start_x + np.argmax(counts)

    return best_line_x, rotated_image


def divide_image(image, bias):
    best_line_x, rotated_image = find_best_division_line(image, bias)
    left_page = rotated_image[:, :best_line_x]
    right_page = rotated_image[:, best_line_x:]
    return left_page, right_page


# endregion


# region Process Images
def divide_all_images_in_folder(input_folder, output_folder, bias):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        page_number = int(filename.split("_")[-1].split(".")[0])
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Image {image_path} not found")
            continue
        left_page, right_page = divide_image(image, bias)
        cv2.imwrite(
            os.path.join(output_folder, f"page_{page_number * 2 - 1}.png"), left_page
        )
        cv2.imwrite(
            os.path.join(output_folder, f"page_{page_number * 2}.png"), right_page
        )
        print(f"Processed {filename}")


def convert_all_pdf_to_image(raw_img_folder_path, output_folder, bias):
    for foldername in os.listdir(raw_img_folder_path):
        print(f"Processing {foldername}")
        input_folder = os.path.join(raw_img_folder_path, foldername)
        output_subfolder = os.path.join(output_folder, foldername)
        divide_all_images_in_folder(input_folder, output_subfolder)


# endregion

# folder with raw images from pdf pages
RAW_IMAGES_FOLDER_PATH = "root"

# folder to save the processed images (cut in half)
EXTRACTED_IMGS_FOLDER = "extracted"

# convert_all_pdf_to_image(RAW_IMAGES_FOLDER_PATH, EXTRACTED_IMGS_FOLDER)
divide_all_images_in_folder(
    "root/Sach-Nom-Cong-Giao-1995-002", "extracted/Sach-Nom-Cong-Giao-1995-002", 0.02
)

# bias for 002: 0.02
