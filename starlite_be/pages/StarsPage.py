from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from time import sleep

from pages.BasePage import BasePage
from pages.CoursePage import CoursePage
from tools.encryption import Encryption
from tools.authentication import set_encrypted_account

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
        self._encryption = Encryption()
        self.last_search = 'Enter Keywords or Course Code'
    
    def login(self, key, username=None, password=None):
        try:
            print("Assert")
            assert self._encryption.set_key(key)
            
            if not self._encryption.decrypt_data(): 
                # If no data, set data
                print("No data found")
                set_encrypted_account(self._encryption, username, password)
            
            input = self.driver.find_element(*self.selector["username-field"])
            input.send_keys(self._encryption.decrypt_data().split(',')[0].strip())  # Get username
            self.driver.find_element(*self.selector["submit-btn"]).click()

            input = self.driver.find_element(*self.selector["password-field"])
            input.send_keys(self._encryption.decrypt_data().split(',')[1].strip()) # Get password
            self.driver.find_element(*self.selector["submit-btn"]).click()

            self.driver.find_element(*self.selector["view-courses-btn"]).click()
        except Exception as e:
            print("Username or password wrong! Please try again.")
            return False
        return True
    
    def get_data(self, courses):
        course_datas = {}
        for course in courses:
            input_ele = self.driver.find_element(*self.selector["subject-textfield"])
            input_ele.clear()
            input_ele.send_keys(course)
            self.last_search = course
            self.driver.find_element(*self.selector["search-btn"]).click()
            
            url = self.driver.find_element(*self.selector["url"]).get_attribute('src')
            coursepage = self.open_course(url, CoursePage)
            data = coursepage.lower_info.split("\n")
            course_datas.update({course:coursepage.get_course_info(data)})
            self.close_other_windows()
        return course_datas