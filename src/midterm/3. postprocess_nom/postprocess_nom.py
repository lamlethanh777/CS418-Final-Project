import json
import os
import re
import ast
import numpy as np
from nom_ocr import load_ocr_results_from_json_dir

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

# Function to filter boxes by Y-coordinate deviation
def filter_boxes_by_y_deviation(boxes, y_threshold_ratio=0.15, x_tolerance = 20):
    # Calculate the average Y-coordinates of the middle third of boxes
    sorted_boxes = sorted(boxes, key=lambda box: (box["points"][0][1] + box["points"][1][1]) / 2)
    num_boxes = len(sorted_boxes)
    if num_boxes < 4:
        return boxes
    middle_third = sorted_boxes[num_boxes // 3 : 2 * num_boxes // 3]
    
    top_y_coordinates = [(box["points"][0][1] + box["points"][1][1]) / 2 for box in middle_third]
    average_y = np.mean(top_y_coordinates)

    # Calculate the threshold for filtering
    y_threshold = average_y * y_threshold_ratio

    avg_x_coordinates = [(box["points"][0][0] + box["points"][1][0] + box["points"][2][0] + box["points"][3][0]) / 4 for box in boxes]
    min_x = min(avg_x_coordinates)
    max_x = max(avg_x_coordinates)

    filtered_boxes = []
    for box in boxes:
        box_y = (box["points"][0][1] + box["points"][1][1]) / 2
        x_average = (box["points"][0][0] + box["points"][1][0] + box["points"][2][0] + box["points"][3][0]) / 4

        if abs(box_y - average_y) > y_threshold:
            if abs(x_average - min_x) < x_tolerance or abs(x_average - max_x) < x_tolerance:
                continue
        filtered_boxes.append(box)
    
    return filtered_boxes

ocr_results = load_ocr_results_from_json_dir("../OCR_NOM/Sach-Nom-Cong-Giao-1995-049")

output_dir = "../OCR_NOM/Sach-Nom-Cong-Giao-1995-049_Processed"
create_output_dir(output_dir)


for page_num, boxes in ocr_results.items():
    print(f"Processing page {page_num}...")

    sorted_boxes = sort_boxes(boxes)

    filtered_boxes = filter_boxes_by_area(sorted_boxes, threshold_ratio=0.1)

    filtered_boxes = filter_boxes_by_y_deviation(filtered_boxes, y_threshold_ratio=0.15)

    output_file = os.path.join(output_dir, f"page_{page_num}.json")
    output_data = {
        "page": page_num,
        "result": filtered_boxes
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Saved: {output_file}")
