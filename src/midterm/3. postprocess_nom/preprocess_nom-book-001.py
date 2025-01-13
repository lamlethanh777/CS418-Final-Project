import json
import os
import re
import ast
import numpy as np
from nom_ocr import load_ocr_results_from_json_dir

def create_output_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_box_coordinates(box):
    points = box["points"]
    avg_x = sum(point[0] for point in points) / len(points)
    avg_y = sum(point[1] for point in points) / len(points)
    return avg_x, avg_y


def get_box_area(box):
    points = box["points"]
    width = abs(points[1][0] - points[0][0])
    height = abs(points[3][1] - points[0][1])
    return width * height

<<<<<<< HEAD:src/midterm/3. postprocess_nom/preprocess_nom-book-001.py

=======
# Function to arrange boxes
>>>>>>> Cuon001:src/preprocess_nom.py
def sort_boxes(boxes, epsilon = 7):
    def compare_with_tolerance(box1, box2):
        x1, y1 = get_box_coordinates(box1)
        x2, y2 = get_box_coordinates(box2)

        if abs(x1 - x2) <= epsilon:
            return y1 - y2
        return x2 - x1

    from functools import cmp_to_key
    return sorted(boxes, key=cmp_to_key(compare_with_tolerance))


def filter_boxes_by_area(boxes, threshold_ratio=0.05):
    areas = [get_box_area(box) for box in boxes]
    average_area = np.mean(areas)
    min_area_threshold = average_area * threshold_ratio

    filtered_boxes = [box for box in boxes if get_box_area(box) >= min_area_threshold]
    return filtered_boxes

<<<<<<< HEAD:src/midterm/3. postprocess_nom/preprocess_nom-book-001.py

ocr_results = load_ocr_results_from_json_dir(r"D:\CS418-Final-Project\src\Output_OCR_Nom_Sach_001_Rotated")
output_dir = "Output_OCR_Nom_Sach_001_Processed"
=======
# Load dữ liệu OCR
ocr_results = load_ocr_results_from_json_dir(r"D:\CS418-Final-Project\src\Output_OCR_Nom_Sach_001_Rotated")
print(len(ocr_results))
# Tạo thư mục đầu ra
output_dir = "Output_OCR_Nom_Sach_001_Processed_Rotated"
>>>>>>> Cuon001:src/preprocess_nom.py
create_output_dir(output_dir)


for page_num, boxes in ocr_results.items():
    print(f"Processing page {page_num}...")

    sorted_boxes = sort_boxes(boxes)

    filtered_boxes = filter_boxes_by_area(sorted_boxes, threshold_ratio=0.1)

    output_file = os.path.join(output_dir, f"page_{page_num}.json")
    output_data = {
        "page": page_num,
        "result": filtered_boxes
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Save {output_file}")
