import os
import fitz
import cv2

DATA_FOLDER = r"../raw"
EXTRACTED_IMGS = r"../extracted_imgs"

import cv2
import numpy as np
import math
from scipy.ndimage import interpolation as inter
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate

# region Divide Image
def detect_skew_angle(image):
    # Use edge detection to highlight text lines
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    if lines is None:
        return 0  # If no lines detected, assume no skew

    # Compute the angles of detected lines
    angles = []
    for rho, theta in lines[:, 0]:
        angle = theta - np.pi / 2
        angles.append(angle)

    # Compute the median angle to reduce the effect of outliers
    median_angle = np.median(angles)
    print(median_angle)
    return median_angle

def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    # Check if the image is grayscale or color
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image  # Already grayscale

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    print(best_angle)
    return best_angle, corrected


def find_best_division_line(image_path):
    # Load the image in color
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Get the skew angle of the image
    skew_angle = get_angle(gray)
    print(f"Skew angle: {skew_angle}")

    # Correct the skew by rotating the image
    rotated_image = rotate(image, skew_angle)

    # Get the image dimensions
    height, width = rotated_image.shape[:2]

    # The division line is at the center of the image
    best_line_x = width // 2

    return best_line_x, rotated_image

def divide_image(image_path):
    # Find the best division line and get the rotated image
    best_line_x, rotated_image = find_best_division_line(image_path)

    # Split the rotated image into two halves
    left_page = rotated_image[:, :best_line_x]
    right_page = rotated_image[:, best_line_x:]
    
    return left_page, right_page

# endregion

# region Convert PDF to Image
def convert_pdf_to_image(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    for page in doc:
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat)
        os.makedirs(output_folder, exist_ok=True)
        image_path = os.path.join(output_folder, f"page_{page.number + 1}.png")
        pix.save(image_path)
        print(f"Page {page.number + 1} saved to {image_path}")
        left, right = divide_image(image_path)
        cv2.imwrite(os.path.join(output_folder, f"page_{page.number * 2 + 1}.png"), left)
        cv2.imwrite(os.path.join(output_folder, f"page_{page.number * 2 + 2}.png"), right)
        # delete the original image
        os.remove(image_path)


def convert_all_pdf_to_image(pdf_folder_path, output_folder):
    """
    Converts all PDF files in the specified folder to images and saves them in the output folder.

    Args:
        pdf_folder_path (str): The path to the folder containing PDF files.
        output_folder (str): The path to the folder where the converted images will be saved.

    Returns:
        None
    """
    for filename in os.listdir(pdf_folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, filename)
            pdf_output_folder = os.path.join(EXTRACTED_IMGS, os.path.splitext(filename)[0])
            convert_pdf_to_image(pdf_path, pdf_output_folder)  
            print(f"PDF {pdf_path} converted to images in {pdf_output_folder}")      
# endregion

convert_all_pdf_to_image("../raw", EXTRACTED_IMGS)