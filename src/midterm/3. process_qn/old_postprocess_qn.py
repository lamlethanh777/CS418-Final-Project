import json
import os
import re
import string
import pandas as pd

def load_dictionary(file_path):
    df = pd.read_excel(file_path)
    dictionary = set(df.iloc[:, 0])
    return dictionary


def split_word_recursive(word, dictionary):
    result = []
    
    def backtrack(start, current_result):
        if start == len(word):
            result.append(current_result[:])
            return
        
        for end in range(len(word), start, -1):
            candidate = word[start:end]
            normalized_candidate = re.sub(r'[^\w\s]', '', candidate).lower()
            if normalized_candidate in dictionary:
                current_result.append(normalized_candidate)
                backtrack(end, current_result)
                current_result.pop()
    backtrack(0, [])
    return result[0] if result else [word]

def processWords(tokenized_words, dictionary):
    output_words = []
    for word in tokenized_words:
        prefix = re.match(r'^\W*', word).group()
        suffix = re.match(r'.*?(\W*)$', word).group(1)
        original_case = re.sub(r'[^\w\s]', '', word)
        
        clean_word = original_case.lower()
        
        if clean_word in dictionary:
            output_words.append(prefix + original_case + suffix)
        else:
            split_result = split_word_recursive(clean_word, dictionary)
            
            def apply_original_case(original, split_words):
                formatted_words = []
                original_letters = list(original)
                current_index = 0
                
                for split_word in split_words:
                    formatted_word = ""
                    for char in split_word:
                        if current_index < len(original_letters) and original_letters[current_index].isupper():
                            formatted_word += char.upper()
                        else:
                            formatted_word += char.lower()
                        current_index += 1
                    formatted_words.append(formatted_word)
                return formatted_words
            
            formatted_split = apply_original_case(original_case, split_result)
            output_words.append(prefix + ' '.join(formatted_split) + suffix)
    
    return output_words


def processText(input_text, dictionary):
    words = input_text.split(' ')
    output_words = processWords(words, dictionary)
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
    # Remove (102a) (la) (2b) etc.
    text = re.sub(r'\(\s*[a-zA-Z0-9l]+\s*\)', '', text)
    # # remove (a), (2)
    # text = re.sub(r"\(\s*([0-9a-zA-Z]+)\s*\)", " ", text)
    # remove - 24 -
    text = re.sub(r"-\s*\d+\s*-", "", text)
    # remove 8.
    text = re.sub(r"\d+\.", "", text)
    # remove roman heading only not in the middle of a sentence
    text = re.sub(r"\b[IVXLCDM]+\b", "", text)
    # # remove standalone consonants including 'i'
    # text = re.sub(r"\s+[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZiI]\s+", "", text)
    # Remove standalone consonants and vowels (e.g., 'i', 'a') surrounded by spaces or punctuation
    text = re.sub(r"\b[iIaA]\b", "", text)

    # Remove standalone consonants (including 'i') that are surrounded by punctuation
    text = re.sub(r"(?<!\w)[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZiI](?!\w)", "", text)
    # remove multiple repeated punctuations
    text = re.sub(r'([^\w\s])\1+', r'\1', text)
    # remove multiple spaces after/before open parentheses, brackets, or braces
    text = re.sub(r'\s*([(\[{])\s+', r' \1', text)
    # remove multiple spaces before/after close parentheses, brackets, or braces or other punctuations
    text = re.sub(r'\s+([)\]}!?,.:;])\s*', r'\1 ', text)
    # remove brackets that are empty or contain only punctuations and spaces
    text = re.sub(r'\([' + re.escape(string.punctuation) + r'\s]*\)', '', text)
    # remove lines that start with a pattern like (1), (2), (3b), etc.
    text = re.sub(r'^\(\s*[a-zA-Z0-9l]+\s*\).*\n?', '', text, flags=re.MULTILINE)
    # remove lines that contain standalone text within parentheses
    text = re.sub(r'^\s*".*"\s*\(.*\)\s*$', '', text, flags=re.MULTILINE)
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
                for i in range(1, 5):
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
input_folder = "../OCR_QN/Sach-Nom-Cong-Giao-1995-049"  # Replace with your input folder path
output_folder = "../OCR_QN/Sach-Nom-Cong-Giao-1995-049_Processed"  # Replace with your output folder path
process_qn_files(input_folder, output_folder)
