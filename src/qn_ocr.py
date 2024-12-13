import json
import os
from google.cloud import vision
from PIL import Image

# Đường dẫn đến thư mục chứa ảnh
images_folder = "../extracted_imgs/Sach-Nom-Cong-Giao-1995-002-cropped"

# Đường dẫn đến tệp Google Cloud Vision API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'nth-wording-440008-v3-5799f3182196.json'

QUOCNGU_CHARSET = 'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ'

# Kiểm tra nếu chuỗi chứa chữ Quốc Ngữ
def is_quoc_ngu(text):
    return any(char in QUOCNGU_CHARSET for char in text)

# Resize hình ảnh để OCR hiệu quả hơn
def resize_image(image_path, max_size=1000):
    with Image.open(image_path) as img:
        width, height = img.size
        total_size = width + height
        if total_size > max_size:
            scale_factor = max_size / total_size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img.save(image_path)
            print(f"Resized image '{image_path}' to {new_width}x{new_height}")

# Thực hiện OCR
def perform_ocr(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0].description
        return [line for line in full_text.splitlines() if is_quoc_ngu(line)]
    else:
        return ["No text detected in the image."]

# Xử lý hình ảnh trong thư mục
def process_images(images_folder, start_page, end_page, output_folder):
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)

    for page_num in range(start_page, end_page + 1):
        image_path = os.path.join(images_folder, f"page_{page_num}.png")

        if not os.path.exists(image_path):
            print(f"Image '{image_path}' not found, skipping...")
            continue
        
        # # Resize ảnh (nếu cần)
        # resize_image(image_path)

        # Thực hiện OCR
        ocr_text = perform_ocr(image_path)
        output_file = os.path.join(output_folder, f"page_{page_num}.json")

        # Tạo cấu trúc JSON và lưu vào file
        json_data = {
            "page": page_num,
            "ocr_text": ocr_text
        }
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"OCR results for page {page_num} saved to '{output_file}'")

# Nhập trang bắt đầu và trang kết thúc
start_page = int(input("Nhập trang bắt đầu: "))
end_page = int(input("Nhập trang kết thúc: "))
output_folder = "Output_OCR_QN"

# Thực hiện xử lý
process_images(images_folder, start_page, end_page, output_folder)