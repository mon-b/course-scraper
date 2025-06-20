import logging
import json

from catalogue_scrapper import catalogue_info
from parity_scrapper import find_course_availability

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def read_course_codes(file_path):
    try:
        with open(file_path, "r") as file:
            course_codes = [line.strip() for line in file.readlines()]
            return course_codes
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    
def write_to_json(data, file_path="results/course_data.json"):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Successfully wrote data to {file_path}")
    except Exception as e:
        logger.error(f"Failed to write JSON: {e}")

def main():

    all_courses = []

    course_codes = read_course_codes("results/course_codes.txt")
    print(course_codes)

    if not course_codes:
        logger.error("No course codes found. Exiting.")
        return
    
    for course_code in course_codes:
        logger.info(f"Processing course code: {course_code}")

        # fetching course details from the catalogue :p
        details = catalogue_info(course_code)

        if not details:
            logger.error(f"\tFailed to fetch details for course code: {course_code}")
            continue

        # check course availability (this is the parity)
        availability = find_course_availability(course_code)

        if not availability:
            logger.error(f"\tNo availability found for course code: {course_code}")
            
            if details:
                if "parity" in details and details["parity"] == "both":
                    details["hide"] = False 

                else:
                    details["hide"] = True
    
        else:

            details["parity"] = availability

        all_courses.append(details)

    print(all_courses)
    write_to_json(all_courses)

if __name__ == "__main__":
    main()