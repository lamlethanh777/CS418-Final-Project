import os
import json
import re

# Hàm để lọc và làm sạch văn bản
def clean_vietnamese_text(text):

    # Loại bỏ các từ trong dấu ngoặc chứa ít nhất một ký tự số
    text = re.sub(r"\([^()]*\d+[^()]*\)", "", text)
    text = re.sub(r"\b\d+[\w]*\)", "", text)

    # Loại bỏ các từ đứng riêng lẻ 1 ký tự trừ nguyên âm tiếng Việt
    vietnamese_vowels = "aáạàảãăắặằẳẵâấầẩẫậeéèẻẽẹêếềểễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵ"
    cleaned_words = [
        word for word in text.split()
        if len(word) > 1 or word.lower() in vietnamese_vowels
    ]

    # Ghép lại văn bản sau khi làm sạch
    return " ".join(cleaned_words)

def process_qn_files(input_folder, output_folder):
    """
    Processes all JSON files in the input folder, cleans the OCR text, and writes the results to the output folder.

    Args:
        input_folder (str): Path to the folder containing input JSON files.
        output_folder (str): Path to the folder where cleaned JSON files will be saved.
    """

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)

            # Read the JSON file
            with open(input_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Process the OCR text and filter out empty strings
            ocr_text = data.get("ocr_text", [])
            # check in the last 5 lines if they start by (1) or (2a)
            if len(ocr_text) > 5:
                for i in range(1, 5):
                    if re.match(r"^\(\s*([\da-zA-Z]*)\s*\)", ocr_text[-i]):
                        ocr_text = ocr_text[:-i]
            cleaned_ocr_text = []
            for line in ocr_text:
                cleaned_line = clean_vietnamese_text(line).strip()
                if cleaned_line:  # Only include non-empty lines
                    cleaned_ocr_text.append(cleaned_line)

            # Prepare the output data
            output_data = {
                "page": data.get("page"),
                "ocr_text": cleaned_ocr_text
            }            

            # Write the cleaned data to the output folder
            output_filename = f"page_{output_data['page']}.json"
            output_path = os.path.join(output_folder, output_filename)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                json.dump(output_data, output_file, ensure_ascii=False, indent=4)

            print(f"Processed and saved: {output_path}")

# Example usage
input_folder = "../OCR_QN/Sach-Nom-Cong-Giao-1995-049_Processed_Gemini"  # Replace with your input folder path
output_folder = "../OCR_QN/Sach-Nom-Cong-Giao-1995-049_Postprocessed_Gemini"  # Replace with your output folder path
process_qn_files(input_folder, output_folder)

# print(clean_vietnamese_text("(13,14,15) — SẮC THỂ CON CHỊU LỄ LẦN ĐẦU."))
# print(clean_vietnamese_text("cầu nguyện cho nó, thì cũng là thói rất trái nghịch;"))
# print(clean_vietnamese_text("Thánh Y ghê ré gia truyền.."))
# print(clean_vietnamese_text("« đạo nam nữ, hễ vừa đến tuổi khôn, thì một năm"))
# print(clean_vietnamese_text("(3,4,5). − SẮC TRẺ CON CHỊU LỄ LẦN ĐẦU. 113"))
# print(clean_vietnamese_text("24) Đây là ví dụ , (không xóa), và ."))