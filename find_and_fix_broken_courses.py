from const import COURSE_DATA
import json
from collections import defaultdict, Counter

import logging
import requests
from bs4 import BeautifulSoup
from const import CATALOGUE_URL

logger = logging.getLogger()

REQUIRED_FIELDS = [
    "SIGLA",
    "CURSO",
    "TRADUCCION",
    "CREDITOS",
    "AREA FG"
]

def check_missing_required_fields():
    with open(COURSE_DATA, "r", encoding="utf-8") as file:
        course_data = json.load(file)

    missing_courses_by_field = defaultdict(list)
    missing_field_counts = Counter()

    for course in course_data:
        missing_fields = [
            field for field in REQUIRED_FIELDS if field != "SIGLA"
            and (field not in course or not str(course[field]).strip())
        ]

        if missing_fields:
            sigla = course.get("SIGLA", "[no SIGLA]")
            name = course.get("CURSO", "[no CURSO]")

            for field in missing_fields:
                missing_courses_by_field[field].append((sigla, name))

            missing_field_counts.update(missing_fields)

    total_broken = sum(len(v) for v in missing_courses_by_field.values())
    logger.info(f"\n⚠️ Found {total_broken} missing field occurrences in courses:\n")

    for field, courses in missing_courses_by_field.items():
        logger.info(f"Field '{field}' missing in {len(courses)} courses:")
        for sigla, name in courses:
            logger.info(f"  • {sigla}: {name}")
        logger.info("")

    if missing_field_counts:
        logger.info("📊 Summary of missing fields:\n")
        for field, count in missing_field_counts.most_common():
            logger.info(f"   - {field}: {count} course(s) missing")

    return missing_courses_by_field, course_data

def fix_area_fg(missing_area_fg, course_data):
    for sigla, _ in missing_area_fg:
        sigla = sigla.strip().upper()

        if sigla.startswith("TTF"):
            area_fg = "Teología"
        elif sigla.startswith("DPT"):
            area_fg = "Salud Y Bienestar"
        elif sigla.startswith("ICP"):
            area_fg = "Ciencias Sociales"
        elif sigla.startswith("ICM"):
            area_fg = "Ciencias Y Tecnologia"
        else:
            area_fg = "Desconocida"

        updated = False
        for course in course_data:
            if course.get("SIGLA", "").strip().upper() == sigla:
                course["AREA FG"] = area_fg
                updated = True
                logger.info(f"Updated AREA FG for {sigla} to '{area_fg}'")
                break

        if not updated:
            logger.warning(f"Warning: course with SIGLA {sigla} not found in data")

def fix_missing_credits(missing_credits, course_data):
    for sigla, name in missing_credits:
        sigla = sigla.strip().upper()
        
        updated = False
        for course in course_data:
            if course.get("SIGLA", "").strip().upper() == sigla:
                course["CREDITOS"] = "10"
                updated = True
                logger.info(f"Updated CREDITOS for {sigla} to 10")
                break
        
        if not updated:
            logger.warning(f"Warning: course with SIGLA {sigla} not found in data")

def fix_missing_translations(missing_translations, course_data):
    logger.info(f"\n📝 Found {len(missing_translations)} courses missing translations")
    logger.info("Enter translations manually (or press Enter to skip):\n")
    
    for i, (sigla, name) in enumerate(missing_translations, 1):
        sigla_clean = sigla.strip().upper()
        
        logger.info(f"[{i}/{len(missing_translations)}]")
        logger.info(f"SIGLA: {sigla_clean}")
        logger.info(f"CURSO: {name}")
        
        translation = input("TRADUCCION: ").strip()
        
        if translation:
            updated = False
            for course in course_data:
                if course.get("SIGLA", "").strip().upper() == sigla_clean:
                    course["TRADUCCION"] = translation
                    updated = True
                    logger.info(f"✅ Updated translation for {sigla_clean}")
                    break
            
            if not updated:
                logger.warning(f"⚠️ Warning: course {sigla_clean} not found in data")
        else:
            logger.info(f"⏭️ Skipped {sigla_clean}")
        
        logger.info("-" * 50)

def save_missing_curso_siglas(course_data, output_file="results/missing_curso_siglas.txt"):
    missing_curso_siglas = []
    
    for course in course_data:
        sigla = course.get("SIGLA", "").strip()
        curso = course.get("CURSO", "").strip()
        
        if not curso:
            missing_curso_siglas.append(sigla if sigla else "[no SIGLA]")
    
    with open(output_file, "w", encoding="utf-8") as f:
        for sigla in missing_curso_siglas:
            f.write(f"{sigla}\n")
    
    logger.info(f"📝 Saved {len(missing_curso_siglas)} SIGLAs missing CURSO to '{output_file}'")
    return missing_curso_siglas

def scrape_course_name_field(course_code):
    url = CATALOGUE_URL + course_code
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except:
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find("pre")
    
    if not content:
        return None
    
    lines = content.text.strip().split("\n")
    
    for line in lines[:15]:
        line = line.strip()
        
        if line.startswith("CURSO:") or line.startswith("CURSO "):
            course_name = line.replace("CURSO:", "").replace("CURSO ", "").strip()
            course_name = course_name.lstrip(":").strip()
            return course_name.title()
            
        elif line.startswith("NOMBRE:") or line.startswith("NOMBRE "):
            course_name = line.replace("NOMBRE:", "").replace("NOMBRE ", "").strip()
            course_name = course_name.lstrip(":").strip()
            return course_name.title()
    
    return None

def fix_missing_curso_by_scraping(missing_curso_siglas, course_data):
    fixed_count = 0
    
    for sigla in missing_curso_siglas:
        if sigla == "[no SIGLA]":
            continue
            
        course_name = scrape_course_name_field(sigla)
        
        if course_name:
            for course in course_data:
                if course.get("SIGLA", "").strip().upper() == sigla.strip().upper():
                    course["CURSO"] = course_name
                    fixed_count += 1
                    break
    
    return fixed_count

def cleanup_broken_courses(course_data):
    original_count = len(course_data)
    courses_to_remove = []
    
    for course in course_data:
        missing_fields = []
        
        if not course.get("SIGLA", "").strip():
            missing_fields.append("SIGLA")
        if not course.get("CURSO", "").strip():
            missing_fields.append("CURSO")
        if not course.get("TRADUCCION", "").strip():
            missing_fields.append("TRADUCCION")
        if not course.get("CREDITOS", "").strip():
            missing_fields.append("CREDITOS")
        if not course.get("AREA FG", "").strip():
            missing_fields.append("AREA FG")
        
        if missing_fields:
            sigla = course.get("SIGLA", "[missing]").strip() or "[missing]"
            curso = course.get("CURSO", "[missing]").strip() or "[missing]"
            
            logger.info(f"\n🔍 Broken course found:")
            logger.info(f"   SIGLA: {sigla}")
            logger.info(f"   CURSO: {curso}")
            logger.info(f"   Missing fields: {', '.join(missing_fields)}")
            
            response = input("Remove this course? (y/n): ").strip().lower()
            
            if response == 'y':
                courses_to_remove.append(course)
                logger.info("✅ Marked for removal")
            else:
                logger.info("👍 Keeping course")
    
    if not courses_to_remove:
        logger.info("✅ No courses removed!")
        return course_data, 0
    
    cleaned_data = [course for course in course_data if course not in courses_to_remove]
    
    logger.info(f"\n🗑️ Removed {len(courses_to_remove)} course(s)")
    return cleaned_data, len(courses_to_remove)

def main():
    missing, course_data = check_missing_required_fields()

    if missing.get("CURSO"):
        curso_siglas = [sigla for sigla, _ in missing["CURSO"]]
        fixed_count = fix_missing_curso_by_scraping(curso_siglas, course_data)
        logger.info(f"✅ Fixed {fixed_count} missing CURSO fields by scraping")

    fix_area_fg(missing["AREA FG"], course_data)
    fix_missing_credits(missing["CREDITOS"], course_data)
    fix_missing_translations(missing["TRADUCCION"], course_data)

    course_data, removed_count = cleanup_broken_courses(course_data)

    save_missing_curso_siglas(course_data)

    with open(COURSE_DATA, "w", encoding="utf-8") as file:
        json.dump(course_data, file, ensure_ascii=False, indent=2)

    logger.info(f"✅ Updated course data saved to {COURSE_DATA}")

    new_missing, _ = check_missing_required_fields()
    
    logger.info(f"Missing AREA FG after cleanup: {len(new_missing.get('AREA FG', []))}")
    logger.info(f"Missing CREDITOS after cleanup: {len(new_missing.get('CREDITOS', []))}")
    logger.info(f"Missing CURSO after cleanup: {len(new_missing.get('CURSO', []))}")

if __name__ == "__main__":
    main()