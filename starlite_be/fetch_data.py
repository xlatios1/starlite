from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from pages.StarsPage import StarsPage
from utils import *
from tools import *
import os

def get_course_data_from_db(courses, database:Local_DB, fernet_key, username=None, password=None, debugged=False):
    courses = [course.upper() for course in courses]
    _db_json = database.load_db()
    assert _db_json['TEST']
    new_course = database.which_data_not_exists(courses, _db_json)
    if new_course:
        chrome_options = Options()
        if not debugged: chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging'])
        chrome_path = '\\'.join(os.path.dirname(__file__).split("\\")[:-1]) + '\\starlite_be\\chromedriver\\chromedriver.exe'
        driver = Chrome(executable_path=chrome_path, options=chrome_options)
        starspage = StarsPage(driver)
        driver.get('https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main')
        while not starspage.login(fernet_key, username, password):
            username, password = None, None
            starspage._encryption.remove_saved_datas()
            driver.get('https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main')
        _db_json.update(starspage.get_data(new_course))
        database.write_db(_db_json)
    return database.query_database(courses, _db_json)

if __name__ == "__main__":
    ldb = Local_DB()
    ldb.reset()
    inputs = ['CZ3005','CZ4045','CZ4023','CZ4042','CZ4041']
    username, password = None, None
    info = get_course_data_from_db(inputs, ldb, 'test', username, password, debugged=True)
    opt = Optimizer(info)
    results = opt.generate_timetable(opt.all_combinations, topn=5)
    assert len(results) == 5
    pass