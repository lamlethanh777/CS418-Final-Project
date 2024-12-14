import json
import os
import re
import string
import pandas as pd

# Hàm đọc từ điển từ file Excel
def load_dictionary(file_path):
    df = pd.read_excel(file_path)
    dictionary = set(df.iloc[:, 0])  # Lấy cột đầu tiên (cột quốc ngữ)
    return dictionary

# Hàm đệ quy để tách từ
def split_word_recursive(word, dictionary):
    result = []
    
    def backtrack(start, current_result):
        if start == len(word):  # Nếu đã duyệt hết từ
            result.append(current_result[:])  # Lưu kết quả
            return
        
        # Duyệt từ dài nhất đến ngắn nhất
        for end in range(len(word), start, -1):  # end giảm dần từ độ dài của từ
            candidate = word[start:end]
            # Chuẩn hóa candidate để tìm trong từ điển
            normalized_candidate = re.sub(r'[^\w\s]', '', candidate).lower()
            if normalized_candidate in dictionary:  # Nếu từ chuẩn hóa này có trong từ điển
                current_result.append(normalized_candidate)  # Thêm từ gốc vào kết quả
                backtrack(end, current_result)  # Tiếp tục với từ tiếp theo
                current_result.pop()  # Quay lại (backtrack)
    # Bắt đầu từ vị trí 0 và danh sách kết quả trống
    backtrack(0, [])
    # Trả về kết quả tìm thấy (nếu có), nếu không thì giữ nguyên từ ban đầu
    return result[0] if result else [word]

def processWords(tokenized_words, dictionary):
    output_words = []
    for word in tokenized_words:
        # Lưu lại định dạng ban đầu của từ
        prefix = re.match(r'^\W*', word).group()  # Ký tự đặc biệt đầu từ
        suffix = re.match(r'.*?(\W*)$', word).group(1)  # Ký tự đặc biệt cuối từ
        original_case = re.sub(r'[^\w\s]', '', word)  # Lưu từ gốc
        
        # Loại bỏ dấu câu và chuyển từ thành chữ thường
        clean_word = original_case.lower()
        
        if clean_word in dictionary:  # Nếu từ đã được làm sạch có trong từ điển
            output_words.append(prefix + original_case + suffix)  # Giữ nguyên định dạng ban đầu
        else:  # Nếu không có, tách từ
            split_result = split_word_recursive(clean_word, dictionary)
            
            # Khôi phục định dạng gốc từng phần của từ
            def apply_original_case(original, split_words):
                formatted_words = []
                original_letters = list(original)  # Tách từng ký tự của từ gốc
                current_index = 0
                
                for split_word in split_words:
                    formatted_word = ""
                    for char in split_word:
                        # Gán định dạng từ gốc (viết hoa/thường)
                        if current_index < len(original_letters) and original_letters[current_index].isupper():
                            formatted_word += char.upper()
                        else:
                            formatted_word += char.lower()
                        current_index += 1
                    formatted_words.append(formatted_word)
                return formatted_words
            
            # Áp dụng định dạng gốc
            formatted_split = apply_original_case(original_case, split_result)
            
            # Ghép các từ lại và thêm vào kết quả (với prefix/suffix ban đầu)
            output_words.append(prefix + ' '.join(formatted_split) + suffix)
    
    return output_words


# Hàm chính
def processText(input_text, dictionary):
    # Split từ theo dấu cách
    words = input_text.split(' ')
    # Xử lý các từ
    output_words = processWords(words, dictionary)

    # Thay dấu gạch nối '-' thành dấu cách ' ' khi đã xử lý xong
    output_text = ' '.join(output_words).replace('-', ' ')
    return output_text


def clean_vietnamese_text(text):
    """
    Cleans Vietnamese text by applying various text normalization techniques.
    Args:
        text (str): The input text to be cleaned.
    Returns:
        str: The cleaned text.
    The function performs the following operations:
    - Removes numbering like 24a, 34b, etc.
    - Removes references like (2) or (a)
    - Removes patterns like (, , , )
    - Removes multiple spaces before a punctuation with space after it
    - Removes consecutive punctuations (at least 2 punctuations)
    - Removes redundant spaces
    - Removes standalone consonants
    - Removes standalone numbers
    - Removes Roman numerals (optional)
    """
    # remove 24a
    text = re.sub(r"\(*\s*(\d+[a-zA-Z])\s*\)*", " ", text)
    # remove (a), (2)
    text = re.sub(r"\(\s*([0-9a-zA-Z]+)\s*\)", " ", text)
    # remove - 24 -
    text = re.sub(r"-\s*\d+\s*-", "", text)
    # remove 8.
    text = re.sub(r"\d+\.", "", text)
    # remove roman heading only not in the middle of a sentence
    text = re.sub(r"\b[IVXLCDM]+\b", "", text)
    # remove standalone consonants
    text = re.sub(r"\s+[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]\s+", "", text)
    # remove multiple repeated punctuations
    text = re.sub(r'([^\w\s])\1+', r'\1', text)
    # remove multiple spaces after/before open parentheses, brackets, or braces
    text = re.sub(r'\s*([(\[{])\s+', r' \1', text)
    # remove multiple spaces before/after close parentheses, brackets, or braces or other punctuations
    text = re.sub(r'\s+([)\]}!?,.:;])\s*', r'\1 ', text)
    # remove brackets that are empty or contain only punctuations and spaces
    text = re.sub(r'\([' + re.escape(string.punctuation) + r'\s]*\)', '', text)
    # remove space before punctuation
    text = re.sub(r'\s+([!?,.:;])', r'\1 ', text)
    # remove standalone punctuations like "-", "'", etc. or if they are at the start or the end of a word
    text = re.sub(r'\s+([!?,.:;\-\'\"])\s+', ' ', text)
    text = re.sub(r'^([!?,.:;\-\'\"])\s+', ' ', text)
    text = re.sub(r'\s+([!?,.:;\-\'\"])$', ' ', text)
    # remove sentence with only punctuations
    text = re.sub(r'^[!?,.:;\-\'\"]+$', '', text)
    # remove multiple consecutive spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()
 

def process_qn_files(input_folder, output_folder):
    """
    Processes all JSON files in the input folder, cleans the OCR text, and writes the results to the output folder.

    Args:
        input_folder (str): Path to the folder containing input JSON files.
        output_folder (str): Path to the folder where cleaned JSON files will be saved.
    """

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load từ điển
    dictionary = load_dictionary("QuocNgu_SinoNom_Dic.xlsx")

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
                for i in range(1, 6):
                    if re.match(r"^\(\s*([\da-zA-Z]*)\s*\)", ocr_text[-i]):
                        ocr_text = ocr_text[:-i]
            cleaned_ocr_text = []
            for line in ocr_text:
                cleaned_line = processText(clean_vietnamese_text(line), dictionary).strip()
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
input_folder = "Output_OCR_QN_Sach_002"  # Replace with your input folder path
output_folder = "Output_OCR_QN_Sach_002_Processed"  # Replace with your output folder path
process_qn_files(input_folder, output_folder)
