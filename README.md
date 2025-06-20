# Course Scraper

A 3 am Python scraper for UC Chile course data. Extracts OFG course codes, fetches details from catalog, determines semester availability.

## Quick Start

```bash
python main.py
```

Outputs `results/course_data.json` with structured course information.

## Configuration

Edit `const.py`:

```python
UPDATE_COURSE_CODES = False  # Re-scrape course codes from web
SAVE_TO_FILE = True          # Save results to files  
REMOVE_DUPLICATES = True     # Filter duplicate codes
```

**Workflow:** Set `UPDATE_COURSE_CODES = True` for first run or new semester, `False` for updates.

## Components

- `ofg_scraper.py`: extracts course codes from OFG pages
- `catalogue_scraper.py`: gets course details from catalog
- `parity_scraper.py`: dtermines semester availability from historical data
- `info_for_course_codes.py`: pipeline orchestrator

## Output

JSON with course code, credits, area, name, and semester availability ("odd"/"even"/"both").

## Notes

- Availability is heuristic based on historical patterns
- Rerun each semester for updates
- Rate limited for server courtesy

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac: venv\Scripts\activate on Windows
pip install -r requirements.txt
```