from PIL import Image
import requests
import fitz
import os
import json

UPLOAD_URL          = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"
CLASSIFICATION_URL  = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-classification"
OCR_URL             = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"

headers = {
    "User-Agent": "test 123",
}

# Bước 1: Tải ảnh lên server
def upload_image(image_path):
    files = {'image_file': open(image_path, 'rb')}
    response = requests.post(UPLOAD_URL, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        if data["is_success"]:
            file_name = data["data"]["file_name"]
            print(f"Upload {file_name} successfully!")
            return file_name
        else:
            print(f"Error upload image: {data['message']}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# Bước 2: Phân loại ảnh (Classification)
def classify_image(file_name):
    data = {"file_name": file_name}
    response = requests.post(CLASSIFICATION_URL, headers=headers, json=data)

    if response.status_code == 200:
        classification_data = response.json()
        if classification_data["is_success"]:
            ocr_name = classification_data["data"]["ocr_name"]
            print(f"Classify Successfully, OCR Name: {ocr_name}")
            return classification_data["data"]["ocr_id"]
        else:
            print(f"Error classification: {classification_data['message']}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# Bước 3: Nhận dạng ký tự từ ảnh (OCR)
def perform_ocr(file_name, ocr_id):
    data = {
        "ocr_id": ocr_id,
        "file_name": file_name
    }
    response = requests.post(OCR_URL, headers=headers, json=data)

    if response.status_code == 200:
        ocr_data = response.json()
        if ocr_data["is_success"]:
            result_text = ocr_data["data"]["result_ocr_text"]
            print(f"OCR Successfully! - {result_text}")
            return result_text
        else:
            print(f"Error OCR: {ocr_data['message']}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None


# Save OCR Results
def save_ocr_result(result_text, output_dir, page_num, is_json=False):
    if is_json:
        result_dict = {"page": page_num, "ocr_text": result_text}
        result_path = os.path.join(
            output_dir, f"page_{page_num}.json")
        with open(result_path, "w", encoding="utf-8") as json_file:
            json.dump(result_dict, json_file, ensure_ascii=False, indent=4)
        print(f"Save OCR SinoNom Successfully: {result_path}")
    else:
        result_path = os.path.join(
            output_dir, f"page_{page_num}.txt")
        with open(result_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(result_text)
        print(f"Save OCR SinoNom Successfully: {result_path}")

def main():
    EXTRACTED_IMGS_DIR  = "./../extracted_imgs"
    OUTPUT_DIR          = "./../Output_OCR_SinoNom"

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    pdf_name = input("Enter PDF file: ").strip()
    pdf_folder_path = os.path.join(EXTRACTED_IMGS_DIR, pdf_name)

    if not os.path.exists(pdf_folder_path):
        print("PDF file does not exist.")
        return

    output_folder = os.path.join(OUTPUT_DIR, pdf_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        start_page  = int(input("First page: "))
        end_page    = int(input("Last page: "))
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
    
    for page_num, image_path in enumerate(image_paths, start = start_page):
        file_name = upload_image(image_path)
        if file_name:
            ocr_id = classify_image(file_name)
            if ocr_id:
                result_text = perform_ocr(file_name, ocr_id)
                if result_text:
                    save_ocr_result(result_text, output_folder, page_num, is_json = True)

    print("OCR SinoNom has been completed successfully.")
 
if __name__ == "__main__":
    main()