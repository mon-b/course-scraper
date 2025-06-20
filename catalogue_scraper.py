import logging
import requests
from bs4 import BeautifulSoup
from const import FIELDS, CATALOGUE_URL


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


def fetch_course_details(course_code):

    url = CATALOGUE_URL + course_code
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find("pre")

    if not content:
        logger.error(f"\tContent not found for course code: {course_code}")
        return
    
    logger.info(f"\tFetched details for course code: {course_code}")
    
    return content.text.strip().split("\n")
    

def get_details(content):

    details = {}

    for line in content:
        for field in FIELDS:
            if field in line:
                # remove field name
                line = line.replace(field, "").strip()
                
                # remove leading colon
                line = line.lstrip(":")

                # capitalize the first letter of each word if it's a name
                if field in ["CURSO", "TRADUCCION", "AREA FG"]:
                    
                    line = line.title()

                details[field] = line

                break

    return details

def new_course(last_line):
    if "2025" in last_line:
        logger.info("\t\tThis course is new for 2025.")
        return True


def catalogue_info(course_code):
    content = fetch_course_details(course_code)

    if not content:
        logger.error(f"\t\tFailed to fetch details for course code: {course_code}")
        return

    details = get_details(content[:12])

    if not details:
        logger.error(f"\t\tNo details found for course code: {course_code}")
        return
    
    is_new = new_course(content[-1])

    if is_new:
        details["parity"] = "both" # this is just a guess tbh

    logger.info(f"\t\t\tDetails for course code {course_code}:")
    logger.info(f"\t\t\t{details}")

    return details

if __name__ == "__main__":

    # some testing never hurt anyone :D
    course_codes = [
        "IIC1103", 
        "IIC100B", 
    ]

    for course_code in course_codes:
        print(catalogue_info(course_code))