import time
import logging
import requests
from bs4 import BeautifulSoup   
from utils.buscacursos_url_constructor import get_first_semester_url, get_second_semester_url

# the goal of this scrapper is to check the availability of courses
# we are using availability data from 2025-1 and 2024-2 semesters
# courses tend to follow a pattern, but information may be incorrect

# information will most certainly be incorrect for new courses
# i mitigated that in the catalogue scrapper by checking if it's a new course
# but this scrapper is just a quick way to check availability, most effective with older courses

# use with caution and always check the official information

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


def find_course_availability(course_code):

    first_semester_url = get_first_semester_url(course_code)

    second_semester_url = get_second_semester_url(course_code)

    logger.info(f"Checking availability for {course_code} in first semester")

    time.sleep(1)

    logger.info("\tFetching ODD availability...")
    odd = fetch_availability(first_semester_url)


    logger.info(f"Checking availability for {course_code} in second semester")

    time.sleep(1)
    
    logger.info("\tFetching EVEN availability...")
    even = fetch_availability(second_semester_url)

    if odd and even:
        logger.info(f"{course_code} is available in both semesters.")
        return "both"
    elif odd:
        logger.info(f"{course_code} is available in the first semester (ODD).")
        return "odd"
    elif even:
        logger.info(f"{course_code} is available in the second semester (EVEN).")
        return "even"


def fetch_availability(url):
    logger.info(f"\t\tConsulting...")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # lol it's so easy ahaha!! thanks to the developers 
    if "La búsqueda no produjo resultados." in soup.text:
        logger.info("\t\tResponse: not available")
        return False
    
    logger.info("\t\tResponse: available")
    return True

def main():
    # testing
    course_codes = [
        "IIC1103", 
        "IIC100B", 
    ]

    for course_code in course_codes:
        find_course_availability(course_code)
        print()


if __name__ == "__main__":
    main()
