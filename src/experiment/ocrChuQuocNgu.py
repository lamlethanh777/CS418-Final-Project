import json
import os
import fitz  # PyMuPDF
from google.cloud import vision
from PIL import Image

# Đường dẫn đến file PDF
pdf_file = "testdata.pdf"

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

def resize_image_byFactor(image_path, scale_factor=2, output_path=None):
    with Image.open(image_path) as img:
        # Tính toán kích thước mới
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        
        # Resize hình ảnh
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Lưu hình ảnh
        save_path = output_path if output_path else image_path
        img_resized.save(save_path)
        
        print(f"Resized image '{image_path}' to {new_width}x{new_height}, saved as '{save_path}'")

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

def process_pdf(pdf_path, start_page, end_page, output_folder):
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)

    # Mở file PDF
    pdf_document = fitz.open(pdf_path)
    for page_num in range(start_page - 1, end_page):
        # Lấy trang hiện tại và render thành hình ảnh
        page = pdf_document[page_num]
        zoom = 2  # Tăng kích thước hình ảnh (2 lần kích thước gốc, tương đương 144 DPI)
        mat = fitz.Matrix(zoom, zoom)  # Ma trận zoom
        pix = page.get_pixmap(matrix=mat)  # Tạo ảnh với độ phân giải cao hơn
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(image_path)
        print(f"Saved page {page_num + 1} as image '{image_path}'")

        # Thực hiện OCR và lưu kết quả vào file JSON
        ocr_text = perform_ocr(image_path)
        output_file = os.path.join(output_folder, f"page_{page_num + 1}.json")

        # Tạo cấu trúc JSON và lưu vào file
        json_data = {
            "page": page_num + 1,
            "ocr_text": ocr_text
        }
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"OCR results saved to '{output_file}'")

# Nhập trang bắt đầu và trang kết thúc
start_page = int(input("Nhập trang bắt đầu: "))
end_page = int(input("Nhập trang kết thúc: "))
output_folder = "Output_OCR_QN"

# Thực hiện xử lý
process_pdf(pdf_file, start_page, end_page, output_folder)
