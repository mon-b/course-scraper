from ofg_scraper import main as ofg_main
from info_for_course_codes import main as info_for_course_codes_main    

def main():
    # in const change flag to True
    ofg_main()

    # i wanted to make a flag for this too but got lazy
    # just comment it out if you don't want to run this
    info_for_course_codes_main() 
    
if __name__ == "__main__":
    main()