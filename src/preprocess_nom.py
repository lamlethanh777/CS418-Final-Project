import json
import os
import re
import ast
import numpy as np

# Function to calculate the average coordinates of a box
def get_box_coordinates(box):
    points = box["points"]
    avg_x = sum(point[0] for point in points) / len(points)
    avg_y = sum(point[1] for point in points) / len(points)
    return avg_x, avg_y

# Function to arrange boxes
def sort_boxes(boxes, epsilon=5):
    def compare_with_tolerance(box1, box2):
        x1, y1 = get_box_coordinates(box1)
        x2, y2 = get_box_coordinates(box2)

        if abs(x1 - x2) <= epsilon:
            return y1 - y2
        return x2 - x1

    from functools import cmp_to_key
    return sorted(boxes, key=cmp_to_key(compare_with_tolerance))