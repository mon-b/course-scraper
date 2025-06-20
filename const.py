# for ofg_scrapper.py
BASE_URL = "https://formaciongeneral.uc.cl/explora-los-cursos/?sf_paged="
TOTAL_PAGES = 61
OUTPUT_FILE = "results/course_codes.txt"

# catalogue url for catalogue_scrapper.py
# just append the course code
CATALOGUE_URL = "https://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo&view=programa&sigla="

# ofg fields for catalogue_scrapper.py
# these are the fields i'll extract and save 
COURSE_CODE = "SIGLA"
CREDITOS = "CREDITOS"
AREA_FG = "AREA FG"
COURSE_NAME = "CURSO"
COURSE_TRANSLATION = "TRADUCCION"
FIELDS = [
    COURSE_CODE,
    CREDITOS,
    AREA_FG,
    COURSE_NAME,
    COURSE_TRANSLATION,
]

# flags
UPDATE_COURSE_CODES = False
SAVE_TO_FILE =  True
REMOVE_DUPLICATES = True