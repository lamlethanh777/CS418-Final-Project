import json
import os
import re
import string
import pandas as pd


def clean_vietnamese_text(text):
    # remove 24a
    text = re.sub(r"\(*\s*(\d+[a-zA-Z])\s*\)*", " ", text)
    # Remove (102a) (la) (2b) etc.
    text = re.sub(r'\(\s*[a-zA-Z0-9l]+\s*\)', '', text)
    # remove - 24 -
    text = re.sub(r"-\s*\d+\s*-", "", text)
    # remove 8.
    text = re.sub(r"\d+\.", "", text)
    # remove roman heading only not in the middle of a sentence
    text = re.sub(r"\b[IVXLCDM]+\b", "", text)
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
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_sentences(ocr_text):
    pattern = r"^\(?-?\d+[a-zA-Z]?\)"
    cleaned_text = [sentence for sentence in ocr_text if not re.match(pattern, sentence.strip())]
    return cleaned_text


def merge_sentences(text_lines):
    merged_lines = []
    i = 0
    while i < len(text_lines):
        if i < len(text_lines) - 1 and not re.search(r'[.,;!?]$', text_lines[i]) and text_lines[i+1][0].islower():
            merged_lines.append(
                text_lines[i].strip() + " " + text_lines[i+1].strip())
            i += 2
        else:
            merged_lines.append(text_lines[i].strip())
            i += 1
    return merged_lines


def process_qn_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)

            with open(input_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            ocr_text = data.get("ocr_text", [])
            ocr_text = clean_sentences(ocr_text)
            ocr_text = merge_sentences(ocr_text)
            cleaned_ocr_text = []
            for line in ocr_text:
                cleaned_line = clean_vietnamese_text(line)
                if cleaned_line:
                    cleaned_ocr_text.append(cleaned_line)
            output_data = {
                "page": data.get("page"),
                "ocr_text": cleaned_ocr_text
            }
            
            output_filename = f"page_{output_data['page']}.json"
            output_path = os.path.join(output_folder, output_filename)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                json.dump(output_data, output_file, ensure_ascii=False, indent=4)

            print(f"Processed and saved: {output_path}")


input_folder    = "Output_OCR_QN_Sach_001" 
output_folder   = "Output_OCR_QN_Sach_001_Processed"
process_qn_files(input_folder, output_folder)
