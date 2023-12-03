from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from pages.StarsPage import StarsPage
from utils import *
from tools import *
import os

def launch_chrome(debugged=False):
    chrome_options = Options()
    if not debugged: chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging'])
    chrome_path = '\\'.join(os.path.dirname(__file__).split("\\")[:-1]) + '\\starlite_be\\chromedriver\\chromedriver.exe'
    driver = Chrome(executable_path=chrome_path, options=chrome_options)
    driver.get('https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main')
    return StarsPage(driver)

def get_course_data(courses:list, database:Local_DB, _encryption:Encryption, debugged=False):
    assert database.data['TEST']
    courses = [course.upper() for course in courses]
    new_course = database.which_data_not_exists(courses)
    course_not_found = []
    if new_course:
        starspage = launch_chrome(debugged)
        try:
            starspage.login(*_encryption.decrypt_data().split(','))
        except:
            ...
        # while not starspage.login(encryption_key):
        #     driver.get('https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main')
        #     username, password = "C200204", "Crystal1_"
        course_datas, course_not_found = starspage.get_data(new_course)
        database.update_db(course_datas, course_not_found)
        starspage.driver.quit()
    return database.query_database(courses)

def validate_account_info(username, password):
    starspage = launch_chrome(debugged=True)
    state = starspage.login(username, password)
    starspage.driver.quit()
    return state

if __name__ == "__main__":
    ldb = Local_DB()
    # ldb.reset()
    inputs = ['CZ4045','CZ3005','CZ4023','CZ4042','CZ4041']
    info, not_found = get_course_data(inputs, ldb,'' ,debugged=True)
    opt = Optimizer(info)
    results = opt.generate_timetable(topn=5)
    assert len(results) == 5
    pass