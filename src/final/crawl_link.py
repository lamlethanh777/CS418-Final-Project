from bs4 import BeautifulSoup
import requests
import re
import json
from urllib.parse import quote
from urllib.parse import unquote

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
    PARAMS['page'] = unquote(url.split("index.php/")[1])
    return S.get(url=MAIN_URL, params=PARAMS)


def has_desired_title(tag, target_title):
    if tag.name == "span" and tag.get("title") == target_title:
        return True
    for child in tag.descendants:
        if child.name == "span" and child.get("title") == target_title:
            return True
    return False


# CRAWL LINKS FROM THE LIBRARY PAGE
response = request_url_content(
    "https://www.hannom-rcv.org/wi/index.php/%E6%9B%B8%E9%99%A2:%E5%BC%B5%E6%AD%A3")
if response.status_code != 200:
    print("Failed to get the content of the page")
    exit()

data = response.json()
html = data['parse']['text']

soup = BeautifulSoup(html, 'html.parser')

a_tags = soup.find_all('a')
links = []

for a_tag in a_tags:
    sibling_count = 0
    match_found = False
    for sibling in a_tag.find_next_siblings():
        if sibling_count >= 2:
            break

        if has_desired_title(sibling, "㐌完成 Đã hoàn thành"):
            links.append(a_tag.get('href'))
            match_found = True
            break

        sibling_count += 1

    if not match_found and sibling_count < 2:
        links.append(a_tag.get('href'))


updated_links = []

for link in links:
    if link:
        response = request_url_content(link)
        if response.status_code != 200:
            print("Failed to get the content of the page")
            exit()

        data = response.json()
        html = data['parse']['text']

        soup = BeautifulSoup(html, 'html.parser')

        redirect_msg = soup.find("div", attrs={"class": "redirectMsg"})

        if redirect_msg:
            redirect_link = redirect_msg.find("a")
            if redirect_link and 'href' in redirect_link.attrs:
                redirect_url = redirect_link['href']
                print(f"Redirect detected: {redirect_url}")
                updated_links.append(redirect_url)
            else:
                print("Redirect message found, but no link available.")
                updated_links.append(link)
        else:
                print("No redirect message found.")
                updated_links.append(link)


with open("library_links.json", "w") as f:
    json.dump(updated_links, f, indent=4)