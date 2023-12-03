# from utils.convert_data_details import convert_data_details
from numpy import dot
from copy import deepcopy

class Optimizer():
    def __init__(self, course_data, morning:int=45000, evening:int=63000):
        self.morning = morning # 12.30pm
        self.evening = evening # 5.30pm
        self._data = course_data
        self.all_combinations = self.get_all_combinations()
        
    def get_all_combinations(self):
        _copy = deepcopy(self._data)
        all_combi = []
        sorted_data = dict(sorted(_copy.items(), key=lambda x:(len(x[1]['Indexes']),x[0])))
        # course_mapping = {idx:course_name for idx, course_name in enumerate(sorted_data.keys())}
        
        for course_name in sorted_data.keys():
            # For each course, add all the index inside
            base_combi = []
            for index, details in _copy[course_name]['Indexes'].items():
                temp = []
                for lessons in details:
                    for hour in range(int(lessons[6][1][0]//3600), int(lessons[6][1][1]//3600)):
                        temp.append(f"{lessons[6][0]}{hour if hour>9 else '0'+str(hour)}")
                base_combi.append([1, [[course_name,index]], temp])
            new_combi = []
            for combi in all_combi: #[[[course,index?], [dtt,dtt]], [[course,index?], [dtt,dtt]]]
                for base_ in base_combi: #[[[course,index], [dtt,dtt]]]
                    if any(item in base_[1] for item in combi[1]):
                        new_combi.append([combi[0], combi[1]+base_[1][0], combi[2]])
                    else:
                        new_combi.append([combi[0]+base_[0],combi[1]+base_[1], base_[2] + combi[2]])
            all_combi+=new_combi+base_combi
        all_combi = sorted(all_combi, reverse=True, key=lambda x:x[0])
        results = [combinations[1] for combinations in all_combi if len(combinations[1])==len(self._data)]
        
        for idx, _combi in enumerate(results):
            temp = []
            for idy, items in enumerate(_combi):
                if len(items)==1:
                    temp+=_combi.pop(idy)
            results[idx] = [_combi, temp] 
        return results

    # def by_date_time(self, setting:list, topn=None):
    #     search = self.all_combinations[:topn]
    #     weights = {idx:[w[-3:] for w in i[1]] for idx,i in enumerate(search)}
    #     for idx, schedule in weights.items():
    #         class_timings = [[0]*7,0,0,0]
    #         for info in schedule:
    #             class_timings[0][int(info[0])] += 1 
    #             if self.morning//3600 < int(info[1:]) < self.evening//3600:
    #                 class_timings[2]+=1
    #             elif int(info[1:]) < self.morning:
    #                 class_timings[1]+=1
    #             else:
    #                 class_timings[3]+=1    
    #         weights[idx] = dot(class_timings[0],setting[0]) + dot(class_timings[1:],setting[1:])
    #     ranking = sorted(weights.items(), key=lambda x:x[1])
    #     return [search[sort_result[0]] for sort_result in ranking]

    def generate_timetable(self, preference=None, topn=None) -> dict:
        def get_acronym(course_title):
            tokens = course_title.split(' ')
            return f"{tokens[0]}({''.join([text[0] for text in tokens[1:]])})"
        # search = [[item[0],list(set(index[:5] for index in item[1]))] for item in self.all_combinations[:topn]]
        # pair_ = {}
        # for idx, options in enumerate(search):
        #     temp = []
        #     for course_title in options[0][0]:
        #         for index in options[1]:
        #             if index in list(self._data[course_title]['Indexes'].keys()):
        #                 temp.append([course_title, index])
        #                 break
        #     pair_[idx] = temp,[conflict_course for conflict_course in options[0][1]]
        results = {}
        for idx, item in enumerate(self.all_combinations[:topn]):
            initialize_parsed_data = [[[] for _ in range(16)] for _ in range(7)]  
            clashes = []    
            exam_dates = []
            course_selected, course_conflict = item
            for matched_details in course_selected:
                acronym = get_acronym(matched_details[0])
                for _class in self._data[matched_details[0]]["Indexes"][matched_details[1]]:
                    timeslot = [int(t) for t in _class[3].split('to')]
                    start_time, duration = timeslot[0], (timeslot[1]//100-timeslot[0]//100)
                    initialize_parsed_data[_class[6][0]][(start_time-830)//100 + 1] = [acronym, _class[0], duration, _class[5]]
                exam_dates.append(f'{acronym}: {self._data[matched_details[0]]["Exam Schedule"][0]}')
            for conflict_class in course_conflict:
                clashes.append(get_acronym(conflict_class))
            results[idx] = {"Conflict": clashes, "Timetable": initialize_parsed_data, "Info": [[get_acronym(c),i]for c,i in self.all_combinations[:topn][idx][0]], "Exam Schedule": exam_dates}
        return results