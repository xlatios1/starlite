from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from time import sleep

from pages.BasePage import BasePage
from pages.CoursePage import CoursePage

class StarsPage(BasePage):
    def __init__(self, driver:WebDriver) -> None:
        super().__init__(driver)
        sleep(2)
        self.selector = {
            "username-field": [By.ID, 'UID'],
            "password-field": [By.ID, 'PW'],
            "submit-btn": [By.XPATH, "//input[@type='submit']"],
            "view-courses-btn": [By.XPATH, "//input[@value='Courses Selection and Info']"],
            "search-btn": [By.XPATH, "//input[@value='Search']"],
            "url": [By.TAG_NAME, "iframe"],
            "subject-textfield": [By.XPATH, "//input[@name='r_subj_code']"],
        }
        self.last_search = 'Enter Keywords or Course Code'
    
    def login(self, username:str, password:str) -> bool:
        try:
            input = self.driver.find_element(*self.selector["username-field"])
            input.send_keys(username.strip())  # Get username
            self.driver.find_element(*self.selector["submit-btn"]).click()

            input = self.driver.find_element(*self.selector["password-field"])
            input.send_keys(password.strip()) # Get password
            self.driver.find_element(*self.selector["submit-btn"]).click()
            assert self.driver.find_element(*self.selector["subject-textfield"]).get_attribute('value') == 'Enter Keywords or Course Code'
            # self.driver.find_element(*self.selector["view-courses-btn"]).click()
        except Exception as e:
            # TODO: handle if account is wrong, unable to use starlite service.
            print(f"Username or password wrong! Please try again. \nError on login msg: {e}")
            return False
        print("Successfully logged in")
        return True
    
    def get_data(self, courses:list) -> dict:
        course_datas = {}
        course_not_found = []
        for course in courses:
            input_ele = self.driver.find_element(*self.selector["subject-textfield"])
            input_ele.clear()
            input_ele.send_keys(course)
            self.last_search = course
            self.driver.find_element(*self.selector["search-btn"]).click()
            
            url = self.driver.find_element(*self.selector["url"]).get_attribute('src')
            self.open_url(url)
            try:
                self.find_element(By.XPATH, "//*[contains(@href,'javascript:view_subject')]").click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                coursepage = CoursePage(self.driver)
                course_name = coursepage.get_course_name()
                course_detail = coursepage.get_course_info()
                course_datas.update({course_name:course_detail})
            except:
                course_not_found.append(course)
            self.close_other_windows()
        return course_datas, course_not_found