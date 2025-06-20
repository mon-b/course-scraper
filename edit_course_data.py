""" 
making the data scraped compatible with the LICCoursePlanner expected format
this is an example of a course read in the planner:

    {
        "id": "COM043",
        "name": "Periodismo de Datos",
        "name_english": "Data Journalism",
        "prereq": "COM117",
        "cred": "10",
        "hide": false,
        "parity": null,
        "type": "optcom",
        "name_stylized": "Periodismo de Datos",
        "number": 44
    }

the number field is a lil dumb.
it'll start on the last course number which is a constant saved in const.py
we need to constantly check the biggest number in the data files 
these are found in LICCoursePlanner/src/data
obviously not ideal, but it works for now

transforming this type of data to the expected format:

    {
        "CURSO": "Apreciacion Del Arte: Modernidad",
        "TRADUCCION": "Art Appreciation: Modernity",
        "SIGLA": "ARO119T",
        "CREDITOS": "10",
        "AREA FG": "Artes",
        "parity": "odd"
    }

"""

import json
from find_and_fix_broken_courses import main as fix_broken_courses

from const import BASE_COURSE_NUMBER, COURSE_DATA, EDITED_COURSE_DATA


def stylize_name(text):

    minor_words = {
        "a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "at", "by", "in", "of", "on", "to", "up", "with", "as",
        "de", "del", "la", "las", "los", "y", "o", "un", "una", "unos", "unas", "al", "el", "en", "por", "con", "sin", "para"
    }

    words = text.title().split()
    result = [words[0]]

    for word in words[1:]:
        if word.lower() in minor_words:
            result.append(word.lower())
        else:
            result.append(word)

    return " ".join(result)


def edit_course_data():
    with open(COURSE_DATA, "r", encoding="utf-8") as file:
        course_data = json.load(file)

    new_course_data = []
    counter = 1

    for course in course_data:
        course_id = course["SIGLA"].strip().upper()

        course_name = course["CURSO"].strip()
        course_name_stylized = stylize_name(course_name)

        course_name_english = stylize_name(course["TRADUCCION"].strip())

        course_cred = course["CREDITOS"].strip()

        course_type = "ofg"  # all courses are ofgs
        course_area = course["AREA FG"].strip() # new field exclusive to ofg

        if "hide" in course.keys():
            course_hide = course["hide"]
        else:
            course_hide = False
        
        if "parity" in course.keys():
            course_parity = course["parity"].strip() if isinstance(course["parity"], str) else course["parity"]
        else:
            course_parity = "both" # probably dumb but whatever

        course_number = BASE_COURSE_NUMBER + counter
        counter += 1

        course_prereq = None # ofgs don't have prerequisites

        new_course = {
            "id": course_id,
            "name": course_name,
            "name_english": course_name_english,
            "prereq": course_prereq,
            "cred": course_cred,
            "hide": course_hide,
            "parity": course_parity,
            "type": course_type,
            "name_stylized": course_name_stylized,
            "number": course_number,
            "area_fg": course_area
        }

        new_course_data.append(new_course)
    
    return new_course_data


def write_course_data():
    data = edit_course_data()

    with open(EDITED_COURSE_DATA, "w", encoding="utf-8") as out:
        json.dump(data, out, ensure_ascii=False, indent=4)


def main():
    fix_broken_courses()
    write_course_data()


if __name__ == "__main__":
    main()
