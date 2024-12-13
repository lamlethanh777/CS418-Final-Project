import pandas as pd
import re


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
            normalized_candidate = standardize_vietnamese(normalized_candidate)
            if normalized_candidate in dictionary:  # Nếu từ chuẩn hóa này có trong từ điển
                current_result.append(normalized_candidate)  # Thêm từ gốc vào kết quả
                backtrack(end, current_result)  # Tiếp tục với từ tiếp theo
                current_result.pop()  # Quay lại (backtrack)
    
    # Bắt đầu từ vị trí 0 và danh sách kết quả trống
    backtrack(0, [])
    
    # Trả về kết quả tìm thấy (nếu có), nếu không thì giữ nguyên từ ban đầu
    return result[0] if result else [word]

# Hàm xử lý danh sách từ
def processWords(tokenized_words, dictionary):
    output_words = []
    for word in tokenized_words:
        if re.search(r'[0-9]',word):
            continue
        if not re.search(r'[a-zA-Z]', word):  # Nếu không có chữ hoặc số
            continue  # Bỏ qua word này
        # Loại bỏ dấu câu và chuyển từ thành chữ thường
        clean_word = re.sub(r'[^\w\s]', '', word).lower()
        clean_word = standardize_vietnamese(clean_word)
        if clean_word in dictionary:  # Nếu từ đã được làm sạch có trong từ điển, giữ nguyên
            output_words.append(word)
        else:  # Nếu không có, tách từ
            split_result = split_word_recursive(word, dictionary)
            output_words.extend(split_result)
    
    return output_words

# Hàm chính
def processText(input_text):
    # Load từ điển
    dictionary = load_dictionary("QuocNgu_SinoNom_Dic.xlsx")
    
    # Split từ theo dấu cách
    words = input_text.split(' ')
    
    # Xử lý các từ
    output_words = processWords(words, dictionary)

    # Thay dấu gạch nối '-' thành dấu cách ' ' khi đã xử lý xong
    output_text = ' '.join(output_words).replace('-', ' ')
    return output_text
