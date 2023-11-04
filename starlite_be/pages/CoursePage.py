from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from time import sleep
from pages.BasePage import BasePage
from collections import defaultdict

class CoursePage(BasePage):
    def __init__(self, driver:WebDriver):
        super().__init__(driver)
        sleep(2) # To prevent slow loading
        self.selector = {
            
        }
        try:
            self.upper_info = self.driver.find_elements(By.TAG_NAME, "tbody")[0].text
            self.lower_info = self.driver.find_elements(By.TAG_NAME, "tbody")[1].text
            self.course_details = self.upper_info.split('\n')[0][4:]
        except:
            self.upper_info = None
            self.lower_info = None
            self.course_details = None
            
    def get_course_name(self):
        return ' '.join(self.course_details.split(" ")[:-3])
    
    def get_course_au(self):
        return ' '.join(self.course_details.split(" ")[-3:-2])
    
    def get_course_info(self, data):
        # {Course name": 'CZ3005 ARTIFICIAL INTELLIGENCE',
        # index: [[type,group,day,time,venue,remark], [type,group,day,time,venue,remark]],
        # index: [[type,group,day,time,venue,remark], [type,group,day,time,venue,remark]],}
        course_info = defaultdict(list)
        course_info = {"Course name": self.get_course_name()}
        for row in data[1:]:
            row_data = row.split(' ')
            if row_data[1]: course_index = row_data[1]
            course_info.setdefault(course_index, []).append(row_data[2:8])
        return course_info