from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
from collections import defaultdict
from re import findall
from datetime import timedelta

class CoursePage(BasePage):
    def __init__(self, driver:WebDriver):
        super().__init__(driver)
        self.wait_for_element(By.TAG_NAME, "tbody")
        self.selector = {}
        try:
            self.upper_info = self.driver.find_elements(By.TAG_NAME, "tbody")[0].text
            self.lower_info = self.driver.find_elements(By.TAG_NAME, "tbody")[1].text
            self.course_details = self.upper_info.split('\n')[0][4:]
        except:
            self.upper_info = None
            self.lower_info = None
            self.course_details = None
            
    def get_course_name(self)->str:
        return ' '.join(self.course_details.split(" ")[:-3])
    
    def get_course_au(self)->str:
        return ' '.join(self.course_details.split(" ")[-3:-2])
    
    def get_exam_date(self)->str:
        return findall("Exam Schedule: .*", self.upper_info)[0].split(":")[1].strip()
    
    def get_course_info(self):
        # {'Exam Schedule': ['29-Apr-2024 1300to1500 hrs', [46800.0, 54000.0]]
        # 'Fixed class': [] or [[type,group,day,time,venue,remark,[day,time,wks]]]
        # 'Indexes': {
            # index1: [[type,group,day,time,venue,remark,[day,time,wks]], 
            #          [type,group,day,time,venue,remark,[day,time,wks]]],
            # index2: [[type,group,day,time,venue,remark,[day,time,wks]], 
            #          [type,group,day,time,venue,remark,[day,time,wks]]],
        # }
        index_info = defaultdict(list)
        exam_time = self.get_exam_date().split(" ")[1]
        course_info = {"Exam Schedule": [self.get_exam_date(), self.convert_time(exam_time)],
                       "Fixed class": [],
                       "Indexes": None
                       }
        for row in self.lower_info.split("\n")[1:]:
            row_data = row.split(' ', 7)
            if row_data[1]: course_index = row_data[1]
            index_info.setdefault(course_index, []).append(
                [data.strip() for data in row_data[2:8]] +
                [[self.convert_date(row_data[4]),
                            self.convert_time(row_data[5]),
                            self.convert_remarks(row_data[7])]])
        course_info['Indexes'] = dict(index_info)
        
        index_values = list(course_info['Indexes'].values())
        for classes in index_values[0]:
            is_same_class = True
            for index_classes in [[parsed_data[6] for parsed_data in index_classes] for index_classes in index_values]:
                if classes[6] not in index_classes: 
                    is_same_class = False
                    break
            if is_same_class: 
                course_info["Fixed class"].append(classes)
        return course_info
    
    def convert_time(self, info:str):
        '''Expects input to be hhmmtohhmm, else returns None'''
        if info[4:6] == "to": return [timedelta(hours=int(c_time[:2]), minutes=int(c_time[2:])).total_seconds() 
                                      for c_time in info.strip().split("to")]
        else: return None
        
    def convert_date(self, info:str):
        '''Expects input to be ddd'''
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        return days.index(info.strip())
    
    def convert_remarks(self, info:str):
        weeks = findall("Wk.*", info)
        if weeks: # Ensure that the remarks are refering to the weeks and not otherwise, default all
            week_detail = weeks[0][2:].split("-")
            if len(week_detail) > 1: # Refers to e.g. "Wk1-10"
                return [i for i in range(int(week_detail[0]), int(week_detail[1])+1)]
            else: # Refers to "Wk3,5,7,9,11,13"
                return [int(i) for i in week_detail[0].split(",")]
        else: # In default, refers to every week
            return []