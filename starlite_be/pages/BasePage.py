from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class BasePage(object):
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.original_window = None
    
    def open_course(self, url, page):
        self.original_window = self.driver.window_handles[0]
        self.driver.execute_script("window.open('', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1]) # The last item in the list is the new window
        self.driver.get(url)
        self.find_element(By.XPATH, "//*[contains(@href,'javascript:view_subject')]").click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return page(self.driver)

    def go_original_window(self):
        self.driver.switch_to.window(self.original_window)
        return self.driver
        
    def close_other_windows(self):
        for window in self.driver.window_handles:
            if window != self.original_window:
                self.driver.switch_to.window(window)
                self.driver.close()
        return self.go_original_window()

        
    def find_element(self, by, identifier):
        return self.driver.find_element(by, identifier)

    def find_elements(self, by, identifier):
        return self.driver.find_elements(by, identifier)

    def wait_for_element(self, by, identifier, buffer=25):
        try:
            return WebDriverWait(self.driver, buffer).until(visibility_of_element_located((by, identifier)))
        except TimeoutException as e:
            return False