import requests
import fitz  # PyMuPDF
import os
import json

# Đặt URL của các API
upload_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"
classification_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-classification"
ocr_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"

# Thêm header "User-Agent" cho request
headers = {
    "User-Agent": "test 123",  # Thay thế User-Agent theo yêu cầu
}

# Bước 1: Tải ảnh lên server
def upload_image(image_path):
    files = {'image_file': open(image_path, 'rb')}
    response = requests.post(upload_url, headers=headers, files=files)
    
    if response.status_code == 200:
        data = response.json()
        if data["is_success"]:
            file_name = data["data"]["file_name"]
            print(f"Tải ảnh lên thành công! Tên file: {file_name}")
            return file_name
        else:
            print(f"Lỗi tải ảnh: {data['message']}")
            return None
    else:
        print(f"Yêu cầu tải ảnh thất bại với mã lỗi: {response.status_code}")
        return None

# Bước 2: Phân loại ảnh
def classify_image(file_name):
    data = {"file_name": file_name}
    response = requests.post(classification_url, headers=headers, json=data)
    
    if response.status_code == 200:
        classification_data = response.json()
        if classification_data["is_success"]:
            ocr_name = classification_data["data"]["ocr_name"]
            print(f"Phân loại ảnh thành công! OCR Name: {ocr_name}")
            return classification_data["data"]["ocr_id"]
        else:
            print(f"Lỗi phân loại ảnh: {classification_data['message']}")
            return None
    else:
        print(f"Yêu cầu phân loại ảnh thất bại với mã lỗi: {response.status_code}")
        return None

# Bước 3: Nhận dạng ký tự từ ảnh (OCR)
def perform_ocr(file_name, ocr_id):
    data = {
        "ocr_id": ocr_id,
        "file_name": file_name
    }
    response = requests.post(ocr_url, headers=headers, json=data)
    
    if response.status_code == 200:
        ocr_data = response.json()
        if ocr_data["is_success"]:
            result_text = ocr_data["data"]["result_ocr_text"]
            print(f"Nhận dạng OCR thành công! Kết quả OCR: {result_text}")
            return result_text
        else:
            print(f"Lỗi OCR: {ocr_data['message']}")
            return None
    else:
        print(f"Yêu cầu OCR thất bại với mã lỗi: {response.status_code}")
        return None

# Chuyển đổi các trang PDF được chọn thành hình ảnh
def pdf_to_image(pdf_path, start_page, end_page, output_dir):
    # Mở PDF bằng PyMuPDF (fitz)
    doc = fitz.open(pdf_path)
    
    # Kiểm tra tính hợp lệ của các trang
    if start_page < 0 or end_page >= doc.page_count or start_page > end_page:
        print("Lỗi: Các trang không hợp lệ.")
        return []

    image_paths = []
    for page_num in range(start_page-1, end_page):  # Chuyển đổi các trang từ start_page đến end_page
        page = doc.load_page(page_num)
        
        # Chuyển trang thành hình ảnh (pixmap)
        pix = page.get_pixmap()
        image_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        
        # Lưu hình ảnh vào file trong thư mục output
        pix.save(image_path)
        image_paths.append(image_path)
    
    return image_paths

# Lưu kết quả OCR vào file .txt hoặc .json
def save_ocr_result(result_text, output_dir, page_num, is_json=False):
    if is_json:
        # Lưu kết quả OCR dưới dạng JSON
        result_dict = {"page": page_num, "ocr_text": result_text}
        result_path = os.path.join(output_dir, f"ocr_result_page_{page_num}.json")
        with open(result_path, "w", encoding="utf-8") as json_file:
            json.dump(result_dict, json_file, ensure_ascii=False, indent=4)
        print(f"Lưu kết quả OCR thành công vào file {result_path}")
    else:
        # Lưu kết quả OCR dưới dạng TXT
        result_path = os.path.join(output_dir, f"ocr_result_page_{page_num}.txt")
        with open(result_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(result_text)
        print(f"Lưu kết quả OCR thành công vào file {result_path}")

# Hàm chính để gọi các bước
def main():
    pdf_path = 'testdata.pdf'  # Đường dẫn đến file PDF của bạn
    output_dir = 'Output_OCR_Nom'  # Đảm bảo thư mục output tồn tại
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    total_pages = 0
    # Nhập vào số trang đầu và trang cuối từ người dùng
    try:
        start_page = int(input("Nhập số trang đầu: "))
        end_page = int(input("Nhập số trang cuối: "))
        total_pages = end_page - start_page + 1
    except ValueError:
        print("Vui lòng nhập số hợp lệ.")
        return

    # Bước 1: Chuyển đổi các trang được chọn trong PDF thành hình ảnh
    image_paths = pdf_to_image(pdf_path, start_page, end_page, output_dir)
    
    if not image_paths:
        print("Không có hình ảnh nào để xử lý.")
        return

    # Tiến hành xử lý OCR cho từng hình ảnh
    for page_num, image_path in enumerate(image_paths):
        # Bước 2: Tải ảnh lên
        file_name = upload_image(image_path)
        if file_name:
            # Bước 3: Phân loại ảnh
            ocr_id = classify_image(file_name)
            if ocr_id:
                # Bước 4: Thực hiện OCR
                result_text = perform_ocr(file_name, ocr_id)
                if result_text:
                    # Lưu kết quả OCR dưới dạng TXT hoặc JSON
                    save_ocr_result(result_text, output_dir, page_num + start_page, is_json=True)  # set is_json=False để lưu dưới dạng TXT

if __name__ == "__main__":
    main()
