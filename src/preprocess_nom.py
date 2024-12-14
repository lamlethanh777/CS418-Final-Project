import json
import os
import re
import ast
import numpy as np
from nom_ocr import load_ocr_results_from_json_dir

# Tạo thư mục nếu chưa tồn tại
def create_output_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to calculate the average coordinates of a box
def get_box_coordinates(box):
    points = box["points"]
    avg_x = sum(point[0] for point in points) / len(points)
    avg_y = sum(point[1] for point in points) / len(points)
    return avg_x, avg_y

# Function to calculate the area of a box
def get_box_area(box):
    points = box["points"]
    width = abs(points[1][0] - points[0][0])
    height = abs(points[3][1] - points[0][1])
    return width * height

# Function to arrange boxes
def sort_boxes(boxes, epsilon=10):
    def compare_with_tolerance(box1, box2):
        x1, y1 = get_box_coordinates(box1)
        x2, y2 = get_box_coordinates(box2)

        if abs(x1 - x2) <= epsilon:
            return y1 - y2
        return x2 - x1

    from functools import cmp_to_key
    return sorted(boxes, key=cmp_to_key(compare_with_tolerance))

# Function to filter boxes based on area
def filter_boxes_by_area(boxes, threshold_ratio=0.05):
    areas = [get_box_area(box) for box in boxes]
    average_area = np.mean(areas)
    min_area_threshold = average_area * threshold_ratio

    filtered_boxes = [box for box in boxes if get_box_area(box) >= min_area_threshold]
    return filtered_boxes

# Load dữ liệu OCR
ocr_results = load_ocr_results_from_json_dir("Output_OCR_Nom_Sach_002")

# Tạo thư mục đầu ra
output_dir = "Output_OCR_Nom_Sach_002_Processed"
create_output_dir(output_dir)

# Xử lý và lưu từng trang
for page_num, boxes in ocr_results.items():
    print(f"Processing page {page_num}...")

    # Sắp xếp các box
    sorted_boxes = sort_boxes(boxes)

    # Lọc các box theo diện tích
    filtered_boxes = filter_boxes_by_area(sorted_boxes, threshold_ratio=0.1)

    # Lưu kết quả vào tệp JSON
    output_file = os.path.join(output_dir, f"page_{page_num}.json")
    output_data = {
        "page": page_num,
        "result": filtered_boxes
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Đã lưu: {output_file}")
