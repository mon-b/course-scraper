import os
import time
import logging
import requests
from bs4 import BeautifulSoup

from const import BASE_URL, TOTAL_PAGES, OUTPUT_FILE, UPDATE_COURSE_CODES, SAVE_TO_FILE, REMOVE_DUPLICATES

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def fetch_page_course_codes(page_num):
    page_url = f"{BASE_URL}{page_num}"
    page_course_codes = []
    
    try:
        # maybe the url is invalid, especially if the total pages change
        logger.info(f"Fetching page {page_num}...")
        response = requests.get(page_url)
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching page {page_num}: {e}")
        return page_course_codes

    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="resultados")

    if not results:
        logger.warning(f"No results found on page {page_num}")
        return page_course_codes

    course_cards = results.find_all("div", class_="uc-card")
    
    if not course_cards:
        logger.warning(f"No course cards found on page {page_num}")
        return page_course_codes

    for card in course_cards:
        span = card.find("span")
        if span:
            # course code will be something like "(IIC1001)"
            # we remove the parentheses
            course_code = span.text.strip().strip("()")
            logger.info(course_code)
            page_course_codes.append(course_code)
    
    logger.info("---------")
    return page_course_codes

def scrape_all_course_codes():
    all_course_codes = []
    
    # this may change in the future
    for i in range(1, TOTAL_PAGES + 1):
        page_course_codes = fetch_page_course_codes(i)
        all_course_codes.extend(page_course_codes)
        time.sleep(1)
    
    return all_course_codes

def save_course_codes(course_codes):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w") as f:
        logger.info(f"Writing {len(course_codes)} course codes to {OUTPUT_FILE}...")
        for course_code in course_codes:
            f.write(f"{course_code}\n")

def main():
    if not UPDATE_COURSE_CODES:
        logger.info("UPDATE_COURSE_CODES is False, skipping scrape")
        return
    
    course_codes = scrape_all_course_codes()
    
    if REMOVE_DUPLICATES:
        original_count = len(course_codes)
        course_codes = list(dict.fromkeys(course_codes))
        if len(course_codes) != original_count:
            logger.info(f"Removed {original_count - len(course_codes)} duplicates")
    
    if SAVE_TO_FILE:
        save_course_codes(course_codes)
    else:
        logger.info(f"Found {len(course_codes)} course code (not saving to file)")
    
    logger.info("Done!")
    return course_codes

if __name__ == "__main__":
    main()