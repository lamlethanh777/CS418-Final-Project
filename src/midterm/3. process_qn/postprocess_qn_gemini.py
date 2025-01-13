import os
import json
import re
import string
import time
import google.generativeai as genai


def clean_vietnamese_text(text):
    """
    Cleans Vietnamese text by applying various text normalization techniques.
    """
    text = re.sub(r"\(*\s*(\d+[a-zA-Z])\s*\)*", " ", text)
    text = re.sub(r'\(\s*[a-zA-Z0-9l]+\s*\)', '', text)
    text = re.sub(r"-\s*\d+\s*-", "", text)
    text = re.sub(r"\d+\.", "", text)
    text = re.sub(r"\b[IVXLCDM]+\b", "", text)
    text = re.sub(r"\b[iIaA]\b", "", text)
    text = re.sub(r"(?<!\w)[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZiI](?!\w)", "", text)
    text = re.sub(r'([^\w\s])\1+', r'\1', text)
    text = re.sub(r'\s*([(\[{])\s+', r' \1', text)
    text = re.sub(r'\s+([)\]}!?,.:;])\s*', r'\1 ', text)
    text = re.sub(r'\([' + re.escape(string.punctuation) + r'\s]*\)', '', text)
    text = re.sub(r'^\(\s*[a-zA-Z0-9l]+\s*\).*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*".*"\s*\(.*\)\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+([!?,.:;])', r'\1 ', text)
    text = re.sub(r'\s+([!?,.:;\-\'\"])\s+', ' ', text)
    text = re.sub(r'^([!?,.:;\-\'\"])\s+', ' ', text)
    text = re.sub(r'\s+([!?,.:;\-\'\"])$', ' ', text)
    text = re.sub(r'^[!?,.:;\-\'\"]+$', '', text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("-", " ")
    return text.strip()


def separate_word(text, prompt_template, model):
    """
    Processes text using a generative AI model.
    """
    prompt = prompt_template.format(input_text=text)
    response = model.generate_content(prompt)
    return response.text


def process_files(input_dir, output_dir, prompt_template, model):
    """
    Processes all files by cleaning and normalizing text in a single step.
    """
    os.makedirs(output_dir, exist_ok=True)

    print("page_9.json".split("_")[1].split(".")[0])

    # sort page name by numerical order
    files = sorted(os.listdir(input_dir), key=lambda x: int(x.split("_")[1].split(".")[0]))

    for filename in files:
        if filename.endswith(".json"):
            # skip if the file is already processed
            if os.path.exists(os.path.join(output_dir, filename)):
                print(f"File {filename} already processed, skipping...")
                continue

            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)

            try:
                # Read the JSON file
                with open(input_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Step 1: Clean text
                ocr_text = data.get("ocr_text", [])
                if len(ocr_text) > 5:
                    for i in range(1, 5):
                        if re.match(r"^\(\s*([\da-zA-Z]*)\s*\)", ocr_text[-i]):
                            ocr_text = ocr_text[:-i]
                cleaned_text = "\n".join([clean_vietnamese_text(line) for line in ocr_text if line.strip()])

                # Step 2: Normalize text using AI
                normalized_text = separate_word(cleaned_text, prompt_template, model)

                # Step 3: Filter normalized text
                normalized_lines = [line.strip() for line in normalized_text.split("\n") if line.strip() and re.search(r'\w', line)]

                # Prepare the output data
                new_data = {
                    "page": data.get("page"),
                    "ocr_text": normalized_lines
                }

                # Write to the output directory
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=4)

                print(f"Processed and saved: {output_file_path}")

            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                print("Retrying after 15 seconds...")
                time.sleep(15)


# Prompt template for the AI model
prompt_template = """
Task: Separate the words
For example:
Input: "amen"
Output: "a men"

Input: "giêsu"
Output: "giê su"

Input: "Yghèrégia"
Output: "Y ghè ré gia"

Input: "Jesu"
Output: "Giê su"

Input: "Maria"
Output: "Ma ri a"

Please not change the position of punctuation. For example: "tôi, một giáo viên" must not return like "tôi , một giáo viên" but return "tôi, một giáo viên"
just return for me the output text, not any other text 

Input: {input_text}
Output:
"""

# Define input and output directories
input_directory = "../OCR_QN/Sach-Nom-Cong-Giao-1995-012"  # Replace with your input folder path
output_directory = "../OCR_QN/Sach-Nom-Cong-Giao-1995-012_Processed_Gemini"  # Replace with your output folder path

# Configure the generative AI modelss
genai.configure(api_key="AIzaSyDzOO6lm7ZJOSVWU6YMaW8U3FWaWH8RpvM")  # Replace with your API key
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Process files
process_files(input_directory, output_directory, prompt_template, model)