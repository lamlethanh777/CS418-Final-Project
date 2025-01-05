from bs4 import BeautifulSoup
import requests
import re
import json
from urllib.parse import quote
from urllib.parse import unquote
import os
import urllib
import google.generativeai as genai

# BASIC FUNCTIONS
# Sino - QN Punctuations
# Sino - QN Characters
nom_punctuation = set('、。.？！')
qn_punctuation = set(',.?!:;')
sino_nom_ranges = [
    (0x3400, 0x4DBF),  # CJK Extension A
    (0x4E00, 0x9FFF),  # CJK Unified Ideographs
    (0xF900, 0xFAFF),  # CJK Compatibility Ideographs
    (0x20000, 0x2A6DF),  # CJK Extension B
    (0x2A700, 0x2B73F),  # CJK Extension C
    (0x2B740, 0x2B81F),  # CJK Extension D
    (0x2B820, 0x2CEAF),  # CJK Extension E
    (0x2CEB0, 0x2EBEF),  # CJK Extension F
    (0x30000, 0x3134F),  # CJK Extension G
]

vietnamese_char_pattern = re.compile(
    r"[aăâáàảãạấầẩẫậắằẳẵặ"
    r"eêéèẻẽẹếềểễệ"
    r"iíìỉĩị"
    r"oôơóòỏõọốồổỗộớờởỡợ"
    r"uưúùủũụứừửữự"
    r"yýỳỷỹỵ"
    r"AĂÂÁÀẢÃẠẤẦẨẪẬẮẰẲẴẶ"
    r"EÊÉÈẺẼẸẾỀỂỄỆ"
    r"IÍÌỈĨỊ"
    r"OÔƠÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢ"
    r"UƯÚÙỦŨỤỨỪỬỮỰ"
    r"YÝỲỶỸỴa-zA-Z]"
)


def is_nom_char(ch):
    return any(start <= ord(ch) <= end for start, end in sino_nom_ranges)


def is_vietnamese_char(ch):
    return vietnamese_char_pattern.search(ch)


MAIN_URL = "https://www.hannom-rcv.org/wi/api.php"
PARAMS = {
    "action": "parse",
    "format": "json",
    "prop": "text|langlinks|links|externallinks|displaytitle|iwlinks|parsewarnings",
    "disableeditsection": "1",
    "disabletoc": "1",
    "formatversion": "2",
    "page": ""
}

S = requests.Session()
S.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'
})

# Specialized function for VI-NA-UY-KI related sites
def request_url_content(url):
    if "index.php/" in url:
        PARAMS['page'] = unquote(url.split("index.php/")[1])
    
        # return the response from the server
        return S.get(url=MAIN_URL, params=PARAMS)
    else:
        response = requests.get(url)
        return response


def get_title_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string


def search_wikisource(title):
    # replace space by underscore
    title = title.replace(" ", "_")
    # urllib encode title
    title = urllib.parse.quote(title)
    search_url = f"http://vi.wikisource.org/w/index.php?title={title}"
    try:
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            no_results_message = soup.find("div", class_="mw-search-nonefound")
            if no_results_message:
                print(f"No results found for title: {title}")
                return None
            else:
                return search_url
        else:
            print(
                f"Search failed for title '{title}', status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Search request failed: {e}")
        return None


def crawl_vietnamese_link(path):
    print(f"Processing: {path}")
    try:
        # Open the local HTML file
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(content, "html.parser")

        # Find the alignment link
        alignment_link = soup.find(
            "a", href=lambda x: x and x.startswith("http://vi.wikisource.org/w/index.php?title=")
        )
        if alignment_link:
            return alignment_link["href"]
    except Exception as e:
        print(f"Error processing {path}: {e}")
    return None


def extract_parallel_titles(soup):
    title = []
    td_element = soup.find('td')
    if td_element:
        nom_titles = []
        viet_titles = []
        current_nom = ''
        current_viet = ''
        
        # Extract Nom and Vietnamese title
        ruby_tags = td_element.find_all('ruby')
        if ruby_tags:
            for ruby in ruby_tags:
                rb = ruby.find('rb')
                rt = ruby.find('rt')
                if rb:
                    current_nom += rb.get_text()
                if rt:
                    current_viet += rt.get_text() + ' '
            nom_titles.append(current_nom.strip())
            viet_titles.append(current_viet.strip())
        else:
            # Extract Nom and Vietnamese title
            mixed_text = td_element.get_text().strip()
            is_adding_nom = is_nom_char(td_element.get_text()[0])
            for ch in mixed_text:
                if is_nom_char(ch):
                    if is_adding_nom:
                        current_nom += ch
                    else:
                        viet_titles.append(current_viet.strip())
                        current_nom = ch
                        is_adding_nom = True
                elif is_vietnamese_char(ch):
                    if not is_adding_nom:
                        current_viet += ch
                    else:
                        nom_titles.append(current_nom.strip())
                        current_viet = ch
                        is_adding_nom = False
                else:
                    if is_adding_nom:
                        current_nom += ch
                    else:
                        current_viet += ch
            if is_adding_nom:
                nom_titles.append(current_nom.strip())
            if current_viet:
                viet_titles.append(current_viet.strip()) 
            
        # return by pair by pair, if one is exhausted, use empty string instead
        joined_nom_titles = ''.join(nom_titles)
        if joined_nom_titles == "詠丐橛":
            viet_titles = ["Vịnh cái quạt"]
        elif joined_nom_titles == "𠳒叫噲同胞吧戰士𪥘󠄁渃":
            viet_titles = ["Lời kêu gọi đồng bào và chiến sĩ cả nước"]

        max_len = max(len(nom_titles), len(viet_titles))
        for i in range(max_len):
            nom = nom_titles[i] if i < len(nom_titles) else ''
            viet = viet_titles[i] if i < len(viet_titles) else ''
            title.append((nom, viet))
    
    return title
    
def extract_parallel_texts(soup):
    sentences_list = []
    has_right_float = False
    divs = soup.find_all('div', style=lambda value: value and 'float:left' in value)
    for div in divs:
        nom_div = div
        viet_div = div.find_next_sibling('div', style=lambda value: value and 'float:right' in value)
        # TODO: Some pages does not have right float div
        if viet_div:
            has_right_float = True
            # Extract texts from p and dt/dd tags
            nom_texts = nom_div.find_all(['p', 'dt', 'dd'])
            viet_texts = viet_div.find_all(['p', 'dt', 'dd'])
            for nom, viet in zip(nom_texts, viet_texts):
                nom_text = nom.get_text(strip=True)
                viet_text = viet.get_text(strip=True)
                sentences_list.append((nom_text, viet_text))
                
    if not has_right_float:
        # All left divs match pair by pair
        divs = soup.find_all('div', style=lambda value: value and 'float:left' in value)
        for i in range(0, len(divs), 2):
            nom_div = divs[i]
            viet_div = divs[i + 1]
            # Extract texts from p and dt/dd tags
            nom_texts = nom_div.find_all(['p', 'dt', 'dd'])
            viet_texts = viet_div.find_all(['p', 'dt', 'dd'])
            for nom, viet in zip(nom_texts, viet_texts):
                nom_text = nom.get_text(strip=True)
                viet_text = viet.get_text(strip=True)
                sentences_list.append((nom_text, viet_text))
                
    return sentences_list


urls = []
with open('library_links.json', 'r', encoding='utf-8') as f:
    urls = json.load(f)

htmls = []
updated_links = []
for i, url in enumerate(urls):
    print(f"Request {i + 1} to {url}")
    response = request_url_content(url)
    print(response.url)
    if response.status_code == 200:
        print(f"Request {i + 1} successful")
        with open(f'tmp_{i + 1}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(response.json(), indent=4, ensure_ascii=False))
        with open(f'tmp_{i + 1}.html', 'w', encoding='utf-8') as f:
            f.write(response.json()['parse']['text'])

        qn_link = crawl_vietnamese_link(f'tmp_{i + 1}.html')
        
        if not qn_link:
            soup = BeautifulSoup(response.json()['parse']['text'], 'html.parser')
            title = extract_parallel_titles(soup)
            if title:
                qn_link = search_wikisource(title[0][1])
                print(f"Search result: {qn_link}")
        
        if qn_link:
            alignment_response = request_url_content(qn_link)
            if alignment_response and alignment_response.status_code == 200:
                alignment_html_path = f"tmp_qn_{i + 1}.html"
                with open(alignment_html_path, "w", encoding="utf-8") as f:
                    f.write(alignment_response.text)
                print(f"Alignment HTML saved to {alignment_html_path}")
            else:
                print(f"Error fetching alignment link: {qn_link}")
        
        updated_links.append({"nom": url, "quocngu": qn_link})
        htmls.append(response.json()['parse']['text'])
    else:
        print(f"Error: Received status code {response.status_code}")

with open("updated_library_links.json", "w", encoding="utf-8") as f:
    json.dump(updated_links, f, ensure_ascii=False, indent=4)

print("Updated library links saved to updated_library_links.json")


prompt_template = """
TÁCH CÁC TỪ TIẾNG VIỆT DÍNH LIỀN NHAU, TRẢ VỀ ĐOẠN VĂN BẢN ĐÃ TÁCH

Input: {input_text}
Output:
"""

genai.configure(api_key="AIzaSyDzOO6lm7ZJOSVWU6YMaW8U3FWaWH8RpvM")  # Replace with your API key
model = genai.GenerativeModel("gemini-2.0-flash-exp")


def split_paragraph_into_sentences(paragraph):
    sentence_endings = r'[。！？,；?：]|……|…'
    
    sentences = re.split(f'({sentence_endings})', paragraph)
    sentences = [s.strip() + (p if p else '') for s, p in zip(sentences[::2], sentences[1::2])]

    filtered_sentences = [
        sentence for sentence in sentences 
        if not re.fullmatch(rf'({sentence_endings})+', sentence.strip())
    ]
    return filtered_sentences


def split_vietnamese_paragraph(paragraph):
    paragraph = re.sub(r'[«»\-]', ' ', paragraph)
    sentence_endings = re.compile(r'(?<=[;!?。.:…])\s*')
    sentences = sentence_endings.split(paragraph)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def box_alignment(s1, s2):
    aligned_s1 = []
    aligned_s2 = []
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    # Fill the DP table for Levenshtein distance
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i == 0:
                dp[i][j] = j  # Cost of insertion
            elif j == 0:
                dp[i][j] = i  # Cost of deletion
            else:
                count_s1 = s1[i - 1]
                count_s2 = s2[j - 1]
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # Deletion
                    dp[i][j - 1] + 1,  # Insertion
                    dp[i - 1][j - 1] + (0 if count_s1 == count_s2 else 1)  # Substitution (only if counts differ)
                )

    # Backtrack to find aligned sequences
    i, j = len(s1), len(s2)
    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            aligned_s1.append(s1[i - 1])
            aligned_s2.append(None)
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            aligned_s1.append(None)
            aligned_s2.append(s2[j - 1])
            j -= 1
        else:
            aligned_s1.append(s1[i - 1])
            aligned_s2.append(s2[j - 1])
            i -= 1
            j -= 1

    aligned_s1.reverse()
    aligned_s2.reverse()

    return aligned_s1, aligned_s2


def count_total_nom(sentence):
    punctuation_pattern = r'[。！？,；?：、]|……|…'
    total_characters = len(sentence)
    
    punctuation_count = len(re.findall(punctuation_pattern, sentence))
    
    result = total_characters - punctuation_count
    
    return result


def pair_sentences_by_length(content, viet):
    content_sentences = []
    viet_sentences = []
    
    for paragraph in content:
        content_sentences.extend(split_paragraph_into_sentences(paragraph))
    
    for paragraph in viet:
        viet_sentences.extend(split_vietnamese_paragraph(paragraph))

    content_lengths = [count_total_nom(sentence) for sentence in content_sentences]
    viet_lengths = [len(sentence.split()) for sentence in viet_sentences]

    aligned_content, aligned_viet = box_alignment(content_lengths, viet_lengths)

    paired_sentences = []

    nom_index = 0
    viet_index = 0
    for index in range(len(aligned_content)):
        matched_nom_sentence = '' if aligned_content[index] is None else content_sentences[nom_index] 
        matched_qn_sentence = '' if aligned_viet[index] is None else viet_sentences[viet_index]

        if aligned_viet[index] is None:
            nom_index += 1
            paired_sentences.append((matched_nom_sentence, matched_qn_sentence))
            continue

        if aligned_content[index] is None:
            viet_index += 1
            paired_sentences.append((matched_nom_sentence, matched_qn_sentence))
            continue
        
        nom_index += 1
        viet_index += 1
        paired_sentences.append((matched_nom_sentence, matched_qn_sentence))
    
    return paired_sentences


def crawl_single_nom_content(html_content):
    full_text = []

    soup = BeautifulSoup(html_content, 'html.parser')
        
    elements = soup.find_all(['p', 'dt', 'dd'])
    
    for element in elements:
        if element.find('a', class_='new'):
            continue 
        text = element.get_text(strip=True)
        if text:
            full_text.append((text, ''))
    
    div_elements = soup.find_all('div', align="right")
    for div_element in div_elements:
        text = div_element.get_text(strip=True)
        if text:
            full_text.append((text, ''))
                
    return full_text


# Crawl from wikisource:
def extract_qn(file_path, class_name='prp-pages-output', tag_name = None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = []

        if tag_name:
            elements = soup.find_all(tag_name)
            for element in elements:
                paragraphs.append(element.get_text(separator=' ', strip=True))
        else:
            content_element = soup.find('div', class_ = class_name)
            if content_element:
                p_elements = content_element.find_all('p')
                for p in p_elements:
                    paragraph_text = p.get_text(separator=' ', strip=True)
                    paragraphs.append(paragraph_text)
            else:
                paragraphs.append("Content not found")
        
        return paragraphs

    except Exception as e:
        return {"error": f"An error occurred: {e}"}


def preprocess_html(html):
    # remove &shy
    html = html.replace('&shy;', '')


def extract_parallel_articles(index, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = extract_parallel_titles(soup)
    content = extract_parallel_texts(soup)
    if not content:
        content = crawl_single_nom_content(html_content)
        nom_sentences = [pair[0] for pair in content]
        if (index + 1) == 8 or (index + 1) == 4 or (index + 1) == 7:
            viet = extract_qn(f'tmp_qn_{index+1}.html', 'prose')
            viet = post_process_qn(viet)
            paired_content = []
            for i, sentence in enumerate(viet):
                paired_content.append((nom_sentences[i], sentence))
            content = paired_content
        elif (index + 1) == 6:
            viet = extract_qn(f'tmp_qn_{index+1}.html', 'poem')
            viet = post_process_qn(viet)
            paired_content = []
            for i, sentence in enumerate(viet):
                paired_content.append((nom_sentences[i], sentence))
            content = paired_content
        elif (index + 1) == 5:
            viet = extract_qn(f'tmp_qn_{index+1}.html')
            viet = post_process_qn(viet)
            nom_sentences = post_process_nom_paragraph(nom_sentences)

            paired_content = pair_sentences_by_length(nom_sentences, viet)
            content = paired_content
        else:
            viet = extract_qn(f'tmp_qn_{index+1}.html')
    
    return {
        'title': title,
        'content': content
    }

def post_process_sentence(sentence):
    # Remove unwanted characters
    sentence = sentence.replace("­", "").replace("-", " ")
    
    # Remove redundant spaces before punctuations
    sentence = re.sub(r'\s+([{}])'.format(re.escape(''.join(qn_punctuation))), r'\1', sentence)

    # Remove redundant spaces
    return ' '.join(sentence.split())


def post_process(article):
    article['title'] = [(post_process_sentence(nom), post_process_sentence(viet)) for nom, viet in article['title']]
    processed_content = []
    if article['content']:
        for nom, viet in article['content']:
            nom = post_process_sentence(nom)
            nom = post_process_nom(nom)
            viet = post_process_sentence(viet)
            processed_content.append((nom, viet))
    
    article['content'] = processed_content
    return article


def remove_vietnamese_words(paragraph):
    vietnamese_word_pattern = r'[a-zA-Z\u00C0-\u1EFF]{2,}'

    return re.sub(vietnamese_word_pattern, '', paragraph)


def post_process_nom(sentence):
    pattern = r'「(.*?)」'
    reference_pattern = r'\[\d+\]'
    extra_pattern = r'|..'

    sentence = re.sub(reference_pattern, '', sentence)
    sentence = re.sub(pattern, r'\1', sentence)
    sentence = remove_vietnamese_words(sentence)
    sentence = sentence.replace('）', ')')
    return sentence


def post_process_nom_paragraph(paragraph):
    return [post_process_nom(sentence) for sentence in paragraph]


def post_process_qn(sentences):
    processed_sentences = []
    invalid_patterns = re.compile(r"^\s*$|⁂")
    reference_pattern = r'\[\s*\d+\s*\]'
    valid_sentences = [sentence for sentence in sentences if not invalid_patterns.match(sentence)]
    for sentence in valid_sentences:
        sentence = re.sub(r"([A-Z]) (\w+)", r"\1\2", sentence)
        sentence = re.sub(r'[«»"“”]', '', sentence)
        sentence = re.sub(reference_pattern, '', sentence)
        sentence = sentence.replace('-', ' ')
        sentence = sentence.replace('...', '…')
        sentence = sentence.replace('\u200b', '')
        processed_sentences.append(sentence.strip())
    
    return processed_sentences

# save result in test dir
if not os.path.exists('test'):
    os.makedirs('test')
for i, html in enumerate(htmls):
    print(f"Extracting {i + 1}")
    
    # Preprocess the html
    preprocess_html(html)
    
    # Extract the parallel articles
    result = extract_parallel_articles(i, html)
    
    # Post-process the result
    result = post_process(result)
    with open(f'test/page_{i + 1}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False))


import html
def html_process(link):
    link = link.replace('&shy;', '')

    soup = BeautifulSoup(link, 'html.parser')
    
    for tag in soup(['script', 'style', 'sup', '.reference']):
        tag.decompose()

html_process(htmls[0])