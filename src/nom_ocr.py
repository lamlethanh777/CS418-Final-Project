from PIL import Image
import requests
import fitz
import os
import json
import time
import random
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys

UPLOAD_URL = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"
CLASSIFICATION_URL = (
    "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-classification"
)
OCR_URL = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"

headers = {
    "User-Agent": "test 123",
}


# Bước 1: Tải ảnh lên server
def upload_image(image_path):
    files = {"image_file": open(image_path, "rb")}
    attempt = 0
    number_of_attempts = random.randint(3, 5)
    upload_success = False

    while not upload_success and attempt < number_of_attempts:
        attempt += 1
        time.sleep(random.randint(1, 5))
        try:
            response = requests.post(UPLOAD_URL, headers=headers, files=files)
        except:
            print("Error: Connection Error")
            print("Retrying...")
            continue

        if response.status_code == 200:
            data = response.json()
            if data["is_success"]:
                file_name = data["data"]["file_name"]
                print(f"Upload {file_name} successfully!")
                return file_name
            else:
                print(f"Error upload image: {data['message']}")
                print("Retrying...")
        else:
            print(f"Error: {response.status_code}")
            print("Retrying...")

    print(f"Failed to upload the image after {number_of_attempts} attempts.")
    return None


# Bước 2: Phân loại ảnh (Classification)
def classify_image(file_name):
    data = {"file_name": file_name}
    attempt = 0
    number_of_attempts = random.randint(3, 5)
    response = requests.post(CLASSIFICATION_URL, headers=headers, json=data)
    classify_success = False

    while not classify_success and attempt < number_of_attempts:
        attempt += 1
        time.sleep(random.randint(1, 5))
        try:
            response = requests.post(CLASSIFICATION_URL, headers=headers, json=data)
        except:
            print("Error: Connection Error")
            print("Retrying...")
            continue

        if response.status_code == 200:
            classification_data = response.json()
            if classification_data["is_success"]:
                classify_success = True
                ocr_name = classification_data["data"]["ocr_name"]
                print(f"Classify Successfully, OCR Name: {ocr_name}")
                return classification_data["data"]["ocr_id"]
            else:
                print(f"Error classification: {classification_data['message']}")
                print("Retrying...")
        else:
            print(f"Error: {response.status_code}")
            print("Retrying...")

    print(f"Failed to classify the image after {number_of_attempts} attempts.")
    return None


# Bước 3: Nhận dạng ký tự từ ảnh (OCR)
def perform_ocr(file_name, ocr_id):
    data = {"ocr_id": ocr_id, "file_name": file_name}
    attempt = 0
    number_of_attempts = random.randint(3, 5)
    ocr_success = False

    while not ocr_success and attempt < number_of_attempts:
        attempt += 1
        time.sleep(random.randint(1, 5))
        try:
            response = requests.post(OCR_URL, headers=headers, json=data)
        except:
            print("Error: Connection Error")
            print("Retrying...")
            continue

        if response.status_code == 200:
            ocr_data = response.json()
            if ocr_data["is_success"]:
                ocr_success = True
                result = ocr_data["data"]["details"]["details"]
                print(f"OCR Successfully! - {ocr_data['data']['result_ocr_text']}")
                return result
            else:
                print(f"Error OCR: {ocr_data['message']}")
                print("Retrying...")
        else:
            print(f"Error: {response.status_code}")
            print("Retrying...")

    print(f"Failed to perform OCR after {number_of_attempts} attempts.")
    return None


# Save OCR Results
def save_ocr_result(result, output_dir, page_num):
    result_dict = {"page": page_num, "result": result}
    result_path = os.path.join(output_dir, f"page_{page_num}.json")
    with open(result_path, "w", encoding="utf-8") as json_file:
        json.dump(result_dict, json_file, ensure_ascii=False, indent=4)
    print(f"Save OCR SinoNom Successfully: {result_path}")


def perform_nom_ocr(pdf_name, start_page, end_page, imgs_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_folder_path = os.path.join(imgs_dir, pdf_name)

    if not os.path.exists(pdf_folder_path):
        print("PDF file does not exist.")
        return

    pdf_base_name = os.path.splitext(pdf_name)[0]
    output_folder = output_dir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        if start_page < 1 or end_page < start_page:
            print("Invalid page range. Please try again.")
            return
    except ValueError:
        print("Please enter valid numbers for the page range.")
        return

    image_paths = []
    for page_num in range(start_page, end_page + 1):
        image_path = os.path.join(pdf_folder_path, f"page_{page_num}.png")
        if not os.path.exists(image_path):
            print(f"Image {image_path} does not exist.")
            return
        image_paths.append(image_path)

    if not image_paths:
        print("No images found for the specified page range.")
        return

    count = 0
    failed = 0
    for page_num, image_path in enumerate(image_paths, start=start_page):
        # check if page is already processed
        if os.path.exists(os.path.join(output_folder, f"page_{page_num}.json")):
            print(f"Page {page_num} has been processed, skipping...")
            continue

        count += 1
        if count % 10 == 0:
            time.sleep(random.randint(10, 15))

        print(f"Processing page {page_num}...")
        file_name = upload_image(image_path)
        if file_name:
            ocr_id = classify_image(file_name)
            if ocr_id:
                result = perform_ocr(file_name, ocr_id)
                if result:
                    save_ocr_result(result, output_folder, page_num)
                    failed = 0
                else:
                    print("OCR failed.")
                    failed += 1
            else:
                print("Classification failed.")
                failed += 1
        else:
            print("Upload failed.")
            failed += 1

        if failed == 5:
            print(f"Failed to process {failed} consecutive pages. Exiting...")
            break

    print(f"OCR SinoNom for {pdf_name} has been completed.")
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle("Task Complete")
    msg_box.setText("Your task has been successfully completed!")
    msg_box.exec_()


def load_ocr_results_from_json_dir(ocr_dir):
    ocr_results = {}
    for file_name in os.listdir(ocr_dir):
        if file_name.endswith(".json"):
            with open(
                os.path.join(ocr_dir, file_name), "r", encoding="utf-8"
            ) as json_file:
                data = json.load(json_file)
                ocr_results[data["page"]] = data["result"]
    return ocr_results


def load_nom_ocr_results_from_extracted_dir(extracted_dir):
    ocr_results = {}
    for pdf_name in os.listdir(extracted_dir):
        if not os.path.isdir(extracted_dir):
            continue
        ocr_results[pdf_name] = load_ocr_results_from_json_dir(extracted_dir)

    return ocr_results



# # Ví dụ sử dụng:
# # Tên thư mục chứa ảnh
# imgs_dir = "../extracted_imgs"
# # Tên thư mục lưu kết quả
# output_dir = "Output_OCR_Nom_Sach_004"
# # Tên PDF
# pdf_name = "Sach-Nom-Cong-Giao-1995-004-cropped"
# # Phạm vi trang
# start_page = 110
# end_page = 111

# perform_nom_ocr(pdf_name, start_page, end_page, imgs_dir, output_dir)