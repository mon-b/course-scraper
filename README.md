# UC Course Scraper

A 3 am Python scraper to extract course information from Universidad Católica's online systems. Built as a supporting tool for the LICCoursePlanner project to generate base course data that can be manually refined and saved to JSON files.

## What it does

1. **Scrapes OFG course codes** from the general education website https://formaciongeneral.uc.cl/
2. **Fetches detailed course info** from the catalog 
3. **Determines semester availability** by checking historical semester data 
4. **Outputs structured JSON** for use in other tools

## Quick Start

```bash
# Run the full pipeline
python main.py
```

This will:
- Scrape all OFG course codes (if `UPDATE_COURSE_CODES = True` in `const.py`)
- Fetch details for each course
- Check availability patterns
- Generate `results/course_data.json`

## Configuration

Edit `const.py` to control behavior:

```python
UPDATE_COURSE_CODES = False  # Set to True to re-scrape course codes from web
SAVE_TO_FILE = True          # Save results to files
REMOVE_DUPLICATES = True     # Remove duplicate course codes
```

### Flag Usage

- **`UPDATE_COURSE_CODES = False`**: Skips the web scraping step and uses existing `course_codes.txt`. Set to `True` when you want to get fresh course codes from the OFG site.

- **`SAVE_TO_FILE = True`**: Saves scraped course codes to `results/course_codes.txt`. Set to `False` if you just want to see the results without saving.

- **`REMOVE_DUPLICATES = True`**: Filters out duplicate course codes before processing. Usually want this `True` unless you're debugging.

**Typical workflow:**
1. First run: Set `UPDATE_COURSE_CODES = True` to build initial course code list
2. Subsequent runs: Keep `UPDATE_COURSE_CODES = False` to reuse existing codes and just update course details
3. New semester: Set `UPDATE_COURSE_CODES = True` again to catch any new courses

## Output Format

Each course in the JSON includes:
- Course code (SIGLA)
- Credits (CREDITOS) 
- General education area (AREA FG)
- Course name and translation
- Semester availability ("odd", "even", "both")
- Whether to hide course if availability uncertain

## Individual Components

### `ofg_scrapper.py`
Extracts course codes from the OFG pages.

### `catalogue_scrapper.py` 
Gets detailed course information from the catalog.

### `parity_scrapper.py`
Determines semester availability by checking 2025-1 and 2024-2 enrollment data.

### `info_for_course_codes.py`
Orchestrates the full data collection pipeline.

## Important Notes

- **Availability data is heuristic** - based on historical patterns, not official schedules
- **Rerun each semester** to update availability patterns and catch new courses
- **Always verify important information** against official sources
- Rate limited to be respectful to UC servers

## Extending

This could easily be extended to scrap different course plans for other majors. LICCoursePlanner could become a universal planner soon if I'm not lazy :p

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment  
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```