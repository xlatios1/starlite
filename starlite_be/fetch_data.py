import requests
from re import findall
from datetime import timedelta, datetime

class FetchData():
    def __init__(self):
        ...
    
    def get_courses(self, course_list):
        datas = {}
        for course in course_list:
            datas.update(self.get_course(course))
        return datas
    
    def get_course(self, course_code):
        GET_COURSE_DETAILS_URL = "https://backend.ntusu.org/modsoptimizer/course_code/"
        data = requests.get(url = GET_COURSE_DETAILS_URL + course_code + '/').json()
        def get_course_name(data):
            return ' '.join([data["code"],data['name']])
        def get_exam_schedule(data):
            exam_schedule = data['get_exam_schedule']
            if exam_schedule:
                datetime = ' '.join([self._convert_date(exam_schedule["date"]), exam_schedule['time'].replace("-",'to').replace(":",""),'hrs'])
                parsed_data = self._convert_time(exam_schedule['time'].replace("-",'to').replace(":",""))
                return [datetime, parsed_data]
            else:
                return ['Not Applicable']
        def get_fixed_class(data):
            fc = []
            for c in data['get_common_information']:
                fc.append(self._convert_info(c))
            return fc
        def get_course_indexes(data):
            ci = {}
            for i in data['indexes']:
                ci.update({str(i['index']) : [self._convert_info(d) for d in i['get_information']]})
            return ci
        
        return {get_course_name(data): {
            'Exam Schedule': get_exam_schedule(data),
            'Fixed Class': get_fixed_class(data),
            'Indexes': get_course_indexes(data)
        }}
    
    def _convert_info(self, info:list):
        return [info['type'].title(),
                info['group'],
                info['day'].title(),
                info['time'].replace("-",'to'),
                info["venue"],
                info['remark'],
                [self._convert_date_to_int(info['day'].title()),
                    self._convert_time(info['time'].replace("-",'to')),
                    self._convert_remarks(info['remark'])]
                ]
    
    def _convert_time(self, info:str):
        '''Expects input to be hhmmtohhmm, else returns None'''
        if info[4:6] == "to": return [timedelta(hours=int(c_time[:2]), minutes=int(c_time[2:])).total_seconds() 
                                      for c_time in info.strip().split("to")]
        else: return None
        
    def _convert_date_to_int(self, info:str):
        '''Expects input to be ddd'''
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        return days.index(info.strip())

    def _convert_date(self, info:str):
        return datetime.strptime(info, "%Y-%m-%d").strftime("%d-%b-%Y")

    def _convert_remarks(self, info:str):
        weeks = findall("Wk.*", info)
        if weeks: # Ensure that the remarks are refering to the weeks and not otherwise, default all
            accumulator = []
            for week in weeks[0][2:].split(","):
                week_detail = week.split("-")
                if len(week_detail) > 1: # Refers to e.g. "Wk1-10"
                    accumulator+=[i for i in range(int(week_detail[0]), int(week_detail[1])+1)]
                else: # Refers to "Wk3,5,7,9,11,13"
                    accumulator+=[int(i) for i in week_detail[0].split(",")]
            return accumulator
        else: # In default, refers to every week
            return []
        