import requests
from bs4 import BeautifulSoup
import re
import json

BASE_URLS = {
    'easy': 'https://sexpositions.club/tag/easy-level',
    'medium': 'https://sexpositions.club/tag/medium-level',
    'hard': 'https://sexpositions.club/tag/hard-level',
    'crazy': 'https://sexpositions.club/tag/crazy',
    # Add more URLs as needed
}

PENETRATION_LEVEL_URLS = {
    'middle': 'https://sexpositions.club/tag/middle-penetration',
    'deep': 'https://sexpositions.club/tag/deep-penetration',
    'shallow': 'https://sexpositions.club/tag/shallow-penetration',
    'without': 'https://sexpositions.club/tag/without-penetration',
}

def get_penetration_level(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful
        page_content = response.text
        
        soup = BeautifulSoup(page_content, 'html.parser')
        pos_tag_div = soup.find('div', class_='pos-tags')
        if pos_tag_div:
            tag_cat_spans = pos_tag_div.find_all('span', id='tag_cat')
            # print(tag_cat_spans)
            for span in tag_cat_spans:
                if span.find('a', href=True):
                    penetration_url = span.find('a', href=True)['href']
                    if penetration_url in PENETRATION_LEVEL_URLS.values():
                        # Extract the penetration level from the URL
                        penetration_level = [k for k, v in PENETRATION_LEVEL_URLS.items() if v == penetration_url][0]
                        name = soup.find('h1', class_='entry-title').text
                        return penetration_level, name
        return None
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_urls_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful
        page_content = response.text
        
        soup = BeautifulSoup(page_content, 'html.parser')
        urls = set()
        
        # Extract URLs from the div with class "post-cards"
        post_cards_div = soup.find('div', class_='post-cards')
        if post_cards_div:
            for link in post_cards_div.find_all('a', href=True):
                href = link['href']
                # Only keep URLs that match the pattern
                if re.match(r'^https://sexpositions.club/positions/\d+\.html$', href):
                    penetration_level, name = get_penetration_level(href)
                    print(f"URL: {href}, Penetration Level: {penetration_level}, Name: {name}")
                    urls.add((href, penetration_level, name))
            
        return list(urls), soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return [], None

def get_next_page(soup):
    next_button = soup.find('a', class_='next page-numbers')
    if next_button:
        return next_button['href']
    return None

if __name__ == "__main__":
    all_urls = {}

    for level, base_url in BASE_URLS.items():
        print(f"Fetching URLs from level '{level}'...")
        current_url = base_url
        urls_list = []

        while current_url:
            urls, soup = get_urls_from_page(current_url)
            urls_list.extend(urls)

            # Get the next page URL
            next_page_url = get_next_page(soup)
            if next_page_url:
                current_url = next_page_url
            else:
                break  # No more pages

        all_urls[level] = urls_list

    # Print all collected URLs with penetration levels
    for level, urls_list in all_urls.items():
        print(f"URLs from level '{level}', found {len(urls_list)}:")
        for url, penetration_level, name in urls_list:
            print(f"URL: {url}, Penetration Level: {penetration_level}, Name: {name}")

	# Write the collected URLs to a JSON file
    with open('sex_positions_urls.json', 'w') as json_file:
        json.dump(all_urls, json_file, indent=4)

    print("URLs written to 'sex_positions_urls.json' file successfully.")