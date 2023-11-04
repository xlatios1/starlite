from utils.convert_data_details import convert_data_details

from numpy import dot
from copy import deepcopy
from collections import defaultdict

class Optimizer():
    def __init__(self, course_data, morning:int=45000, evening:int=63000):
        self.morning = morning # 12.30pm
        self.evening = evening # 5.30pm
        self.all_combinations = self.greedy_combo(course_data, None)
        self._data = course_data

    def greedy_combo(self, course_data, topn=None):
        _copy = deepcopy(course_data)
        convert_data_details(_copy)
        all_combi = []
        _days_arr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        sorted_data = {course:[len(indexes)-1, int(course[2:3]), _copy[course]] for course, indexes in _copy.items()}
        sorted_chance = {k:v[2] for k,v in dict(sorted(sorted_data.items(), key=lambda x:(x[1][0],x[1][1]))).items()}

        course_mapping = {idx:course_name for idx, course_name in enumerate(sorted_chance.keys())}
        for id, course_code in course_mapping.items():
            # For each course, add all the index inside
            base_combi = []
            for index, details in _copy[course_code].items():
                if index!="Course name":
                    temp = []
                    for lessons in details:
                        for hour in range(int(lessons[3][0]//3600), int(lessons[3][1]//3600)):
                            temp.append(f"{index}{_days_arr.index(lessons[2])}{hour if hour>9 else '0'+str(hour)}")
                    base_combi.append([str(id), temp])
            new_combi = []
            for combi in all_combi: #[[id, [idtt,idtt]], [id,[idtt,idtt]]]
                for base_ in base_combi: #[[id, [idtt]]]
                    cur_combi = [i[-3:] for i in combi[1]]
                    cur_base = [i[-3:] for i in base_[1]]
                    if any(True for item in cur_combi if item in cur_base): break
                    new_combi.append([base_[0] + combi[0], base_[1] + combi[1]])
            all_combi+=new_combi+base_combi
        all_combi = sorted(all_combi, reverse=True, key=lambda x:len(x[0]))
        for _combi in all_combi:
            courses_info = [[v for k,v in course_mapping.items() if str(k) in _combi[0]],[v for k,v in course_mapping.items() if str(k) not in _combi[0]]]
            _combi[:] = [courses_info, _combi[1]]
        return all_combi[:topn]

    def by_date_time(self, setting:list, topn=None):
        search = self.all_combinations[:topn]
        weights = {idx:[w[-3:] for w in i[1]] for idx,i in enumerate(search)}
        for idx, schedule in weights.items():
            class_timings = [[0]*7,0,0,0]
            for info in schedule:
                class_timings[0][int(info[0])] += 1 
                if self.morning//3600 < int(info[1:]) < self.evening//3600:
                    class_timings[2]+=1
                elif int(info[1:]) < self.morning:
                    class_timings[1]+=1
                else:
                    class_timings[3]+=1    
            weights[idx] = dot(class_timings[0],setting[0]) + dot(class_timings[1:],setting[1:])
        ranking = sorted(weights.items(), key=lambda x:x[1])
        return [search[sort_result[0]] for sort_result in ranking]

    def generate_timetable(self, preference=None, topn=None):
        def get_acronym(course_code):
            name = self._data[course_code]['Course name']
            return f"{course_code}({''.join([text[0] for text in name.split(' ')[1:]])})"
        search = [[item[0],list(set(index[:5] for index in item[1]))] for item in self.all_combinations[:topn]]
        pair_ = {}
        for idx, options in enumerate(search):
            temp = []
            for course_code in options[0][0]:
                for index in options[1]:
                    if index in list(self._data[course_code].keys()):
                        temp.append([course_code, index])
                        break
            pair_[idx] = temp,[conflict_course for conflict_course in options[0][1]]

        result_data = defaultdict(dict)
        for idx, item in pair_.items():
            course_selected, course_conflict = item
            for course, index in course_selected:
                _course_data = self._data[course]
                result_data[idx].update({course:[_course_data['Course name'][7:].title()] + _course_data[index]})
            for clash_course in course_conflict:
                result_data[idx].update({clash_course:[self._data[clash_course]['Course name'][7:].title()]})
        results = {}
        days_arr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for idx, single_result in result_data.items():
            initialize_parsed_data = [[[] for _ in range(16)] for _ in range(7)]  
            clashes = []    
            for course, info in single_result.items():
                class_name = info[0]
                if len(info) != 1:
                    for _class in info[1:]:
                        timeslot = [int(t) for t in _class[3].split('to')]
                        start_time, duration = timeslot[0], (timeslot[1]//100-timeslot[0]//100)
                        initialize_parsed_data[days_arr.index(_class[2])][(start_time-830)//100 + 1] = [get_acronym(course), _class[0], duration, _class[5]]
                else:
                    clashes.append(get_acronym(course))
            results[idx] = {"Conflict": clashes, "Timetable": initialize_parsed_data, "Info": [[get_acronym(c),i]for c,i in pair_[idx][0]]}
        return results

    
    # def _extract_course_data(self, course_data):
    #     choice_year = {course:[len(indexes)-1, int(course[2:3]), self._copy[course]] for course, indexes in course_data.items()}
    #     datetimings = {}
    #     _days_arr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    #     for course_code, course_info in course_data.items():
    #         datetimings.update({course_code:{}})
    #         for index, lessons in course_info.items():
    #             if index != "Course name":
    #                 class_timings = [[0]*7,0,0,0]
    #                 for info in lessons:
    #                     class_timings[0][_days_arr.index(info[2])]+= 1 
    #                     if self.morning < info[3][1] < self.evening:
    #                         class_timings[2]+=1
    #                     elif info[3][1] < self.morning:
    #                         class_timings[1]+=1
    #                     else:
    #                         class_timings[3]+=1    
    #                 datetimings[course_code].update({index:class_timings})
    #     return [choice_year, datetimings, course_data]
    
    # @pad_back_info
    # def by_time(self, setting):
    #     temp = {}
    #     setting_len = len(setting)-1
    #     def _handle_inner(tup):
    #         key, d = tup
    #         if type(setting)==type([]):
    #             def inner_nested_loop(counter):
    #                 print(f"{index}:","c=", d[0][setting[counter]+1])
    #                 if counter == setting_len:
    #                     return d[setting[counter]+1]
    #                 else:
    #                     return d[setting[counter]+1], inner_nested_loop(counter+1)
    #             print(f"{index}:","initial c=", d[setting[0]+1])
    #             return (d[setting[0]+1], inner_nested_loop(1))
    #         else:
    #             return d[setting+1]
            
    #     def _handle_outer(tup):
    #         key, d = tup
    #         if type(setting)==type([]):
    #             def inner_nested_loop(counter):
    #                 if counter == setting_len:
    #                     return d[list(d.keys())[0]][setting[counter]+1]
    #                 else:
    #                     return d[list(d.keys())[0]][setting[counter]+1], inner_nested_loop(counter+1)
    #             return (d[list(d.keys())[0]][setting[0]+1], inner_nested_loop(1))
    #         else:
    #             return d[list(d.keys())[0]][setting+1]
            
    #     for course, index in self.datas[1].items():
    #         temp[course] = dict(sorted(index.items(), reverse=True,key=_handle_inner))
    #     sorted_timing = dict(sorted(temp.items(), reverse=True, key=_handle_outer))
    #     return {k:list(v.keys()) for k,v in sorted_timing.items()}
    
    # @pad_back_info
    # def by_date(self, setting:list|int):
    #     temp = {}
    #     setting_len = len(setting)-1
    #     def _handle_inner(tup):
    #         key, d = tup
    #         if type(setting)==type([]):
    #             def inner_nested_loop(counter):
    #                 if counter == setting_len:
    #                     return d[0][setting[counter]]
    #                 else:
    #                     return d[0][setting[counter]], inner_nested_loop(counter+1)
    #             return (d[0][setting[0]], inner_nested_loop(1))
    #         else:
    #             return d[0][setting]
            
    #     def _handle_outer(tup):
    #         key, d = tup
    #         if type(setting)==type([]):
    #             def inner_nested_loop(counter):
    #                 if counter == setting_len:
    #                     return d[list(d.keys())[0]][0][setting[counter]]
    #                 else:
    #                     return d[list(d.keys())[0]][0][setting[counter]], inner_nested_loop(counter+1)
    #             return (d[list(d.keys())[0]][0][setting[0]], inner_nested_loop(1))
    #         else:
    #             return d[list(d.keys())[0]][0][setting]
        
    #     for course, index in self.datas[1].items():
    #         temp[course] = dict(sorted(index.items(), reverse=True, key=_handle_inner))
    #     sorted_date = dict(sorted(temp.items(), reverse=True, key=_handle_outer))
    #     print(sorted_date)
    #     return {k:list(v.keys()) for k,v in sorted_date.items()}

# a = {'CZ3005': {'Course name': 'CZ3005 ARTIFICIAL INTELLIGENCE', '10475': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TACD', 'Tue', '1630to1720', 'TR+8', ''], ['Lab', 'TACD', 'Wed', '0830to1020', 'SWLAB3', '']], '10491': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TEL1', 'Wed', '1130to1220', 'TR+7', ''], ['Lab', 'TEL1', 'Tue', '0830to1020', 'SWLAB3', '']], '10493': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TEL3', 'Tue', '1330to1420', 'TR+21', ''], ['Lab', 'TEL3', 'Mon', '1430to1620', 'SWLAB3', '']], '10494': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TEL4', 'Thu', '1130to1220', 'TR+23', ''], ['Lab', 'TEL4', 'Thu', '1230to1420', 'SWLAB3', '']], '10496': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TEL6', 'Thu', '1030to1120', 'TR+4', ''], ['Lab', 'TEL6', 'Wed', '1430to1620', 'SWLAB3', '']], '10560': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TCMA', 'Mon', '1130to1220', 'TR+6', ''], ['Lab', 'TCMA', 'Wed', '1230to1420', 'SWLAB3', '']], '10561': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TDDA', 'Mon', '1630to1720', 'TR+8', ''], ['Lab', 'TDDA', 'Mon', '1230to1420', 'SWLAB3', '']], '10562': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TDDB', 'Tue', '1630to1720', 'TR+33', ''], ['Lab', 'TDDB', 'Mon', '1230to1420', 'SPL', '']], '10563': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TDDC', 'Thu', '1130to1220', 'TR+16', ''], ['Lab', 'TDDC', 'Mon', '1230to1420', 'SPL', '']], '10564': [['Lec/Studio', 'SCL3', 'Mon', '1030to1120', 'LT1A', ''], ['Lec/Studio', 'SCL3', 'Tue', '1230to1320', 'LT1A', ''], ['Tut', 'TCCA', 'Tue', '1630to1720', 'TR+37', ''], ['Lab', 'TCCA', 'Wed', '1030to1220', 'SWLAB3', '']]}, 'CZ4045': {'Course name': 'CZ4045 NATURAL LANGUAGE PROCESSING', '10433': [['Lec/Studio', 'SCL4', 'Wed', '0930to1120', 'LT19', ''], ['Tut', 'SCEL', 'Wed', '1130to1220', 'LT19', '']]}, 'CZ4023': {'Course name': 'CZ4023 ADVANCED COMPUTER NETWORKS', '10427': [['Lec/Studio', 'SCL4', 'Tue', '1530to1720', 'LT8', ''], ['Tut', 'SCEL', 'Fri', '1630to1720', 'LT8', '']]}, 'CZ4042': {'Course name': 'CZ4042 NEURAL NETWORK & DEEP LEARNING', '10431': [['Lec/Studio', 'SCL4', 'Fri', '1130to1320', 'LT1A', ''], ['Tut', 'SCEL', 'Wed', '1730to1820', 'LT1A', '']]}, 'CZ4041': {'Course name': 'CZ4041 MACHINE LEARNING', '10429': [['Lec/Studio', 'SCL4', 'Tue', '1130to1320', 'LKC-LT', ''], ['Tut', 'SCEL', 'Thu', '1330to1420', 'LKC-LT', '']]}}
# pass