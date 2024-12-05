import pandas as pd
import re


# New tone mapping dictionary that groups similar characters together
tone_mapping = {
    "a": ["a", "á", "à", "ả", "ã", "ạ"],
    "â": ["â", "ấ", "ầ", "ẩ", "ẫ", "ậ"],
    "ă": ["ă", "ắ", "ằ", "ẳ", "ẵ", "ặ"],
    "e": ["e", "é", "è", "ẻ", "ẽ", "ẹ"],
    "ê": ["ê", "ế", "ề", "ể", "ễ", "ệ"],
    "i": ["i", "í", "ì", "ỉ", "ĩ", "ị"],
    "o": ["o", "ó", "ò", "ỏ", "õ", "ọ"],
    "ô": ["ô", "ố", "ồ", "ổ", "ỗ", "ộ"],
    "ơ": ["ơ", "ớ", "ờ", "ở", "ỡ", "ợ"],
    "u": ["u", "ú", "ù", "ủ", "ũ", "ụ"],
    "ư": ["ư", "ứ", "ừ", "ử", "ữ", "ự"],
    "y": ["y", "ý", "ỳ", "ỷ", "ỹ", "ỵ"],
}

# Function to detect and standardize Vietnamese tone marks
def standardize_vietnamese(word):
    if not isinstance(word, str):
        return word  # Return the word as is if it's not a string
    tone_number = ""
    base_word = ""
    for char in word:
        found = False
        for base_char, variations in tone_mapping.items():
            if char in variations:
                if variations.index(char) != 0:
                    tone_number = str(variations.index(char))
                base_word += base_char
                found = True
                break
        if not found:
            base_word += char
    # If there's a tone number, append it to the base word
    return base_word + tone_number if tone_number else base_word

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
        # Loại bỏ dấu câu và chuyển từ thành chữ thường
        clean_word = re.sub(r'[^\w\s]', '', word).lower()
        clean_word = standardize_vietnamese(clean_word)
        if clean_word in dictionary:  # Nếu từ đã được làm sạch có trong từ điển, giữ nguyên
            output_words.append(clean_word)
        else:  # Nếu không có, tách từ
            split_result = split_word_recursive(word, dictionary)
            output_words.extend(split_result)
    
    return output_words

# Hàm chính
def processText(input_text):
    # Load từ điển
    dictionary = load_dictionary("Standardized_QuocNgu_SinoNom_Dic.xlsx")
    
    # Split từ theo dấu cách
    words = input_text.split(' ')
    
    # Xử lý các từ
    output_words = processWords(words, dictionary)

    # Thay dấu gạch nối '-' thành dấu cách ' ' khi đã xử lý xong
    output_text = ' '.join(output_words).replace('-', ' ')
    return output_text



# # Load the Excel file
# df = pd.read_excel("./QuocNgu_SinoNom_Dic.xlsx")

# # Apply the standardize_vietnamese function to the 'QuocNgu' column
# df["QuocNgu"] = df["QuocNgu"].apply(standardize_vietnamese)

# # Save the result to the same Excel file
# df.to_excel("./QuocNgu_SinoNom_Dic_Standardize.xlsx", index=False)

# print("Standardized file saved to 'QuocNgu_SinoNom_Dic_Standardize.xlsx'")