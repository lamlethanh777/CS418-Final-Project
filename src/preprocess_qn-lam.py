import re
import string

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
    text = re.sub(r"\(\s*(\d+[a-zA-Z])\s*\)", " ", text)
    # remove (a), (2)
    text = re.sub(r"\(\s*([0-9a-zA-Z]+)\s*\)", " ", text)
    # remove - 24 -
    text = re.sub(r"-\s*\d+\s*-", "", text)
    # remove multiple repeated punctuations
    text = re.sub(r'([^\w\s])\1+', r'\1', text)
    # remove multiple spaces after/before open parentheses, brackets, or braces
    text = re.sub(r'\s*([(\[{])\s+', r' \1', text)
    # remove multiple spaces before/after close parentheses, brackets, or braces
    text = re.sub(r'\s+([)\]}])\s*', r'\1 ', text)
    # remove brackets that are empty or contain only punctuations and spaces
    text = re.sub(r'\([' + re.escape(string.punctuation) + r'\s]*\)', '', text)
    # remove space before punctuation
    text = re.sub(r'\s+([!?,.:;])', r'\1 ', text)
    # remove multiple consecutive spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()