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


def convert_tone_number(word):
    if not isinstance(word, str):
        return word

    tone_number = ""
    base_word = ""

    if word[-1].isdigit():
        tone_number = int(word[-1])
        base_word = word[:-1]
    else:
        base_word = word

    if not tone_number:
        return word

    vowels_in_word = [char for char in base_word if char in tone_mapping]

    if len(vowels_in_word) > 1:
        for base_char, variations in tone_mapping.items():
            if base_char in base_word and base_char not in ["i", "y"]:
                base_word = base_word.replace(
                    base_char, variations[tone_number])
                break
    else:
        for base_char, variations in tone_mapping.items():
            if base_char in base_word:
                base_word = base_word.replace(
                    base_char, variations[tone_number])
                break
        
    return base_word


# # Load the Excel file
# df = pd.read_excel("./QuocNgu_SinoNom_Dic.xlsx")

# # Apply the standardize_vietnamese function to the 'QuocNgu' column
# df["QuocNgu"] = df["QuocNgu"].apply(standardize_vietnamese)

# # Save the result to the same Excel file
# df.to_excel("./Standardized_QuocNgu_SinoNom_Dic.xlsx", index=False)

# print("Standardized file saved to 'Standardized_QuocNgu_SinoNom_Dic.xlsx'")
