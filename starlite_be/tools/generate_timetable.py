from utils.convert_data_details import convert_data_details

from copy import deepcopy

def generate_timetable(course_data):
    def insert_timetable(_timetable_info, _index_info):
        for classes in _index_info:
            timings = classes[3]
            timings.append(classes[5])
            if classes[2] not in _timetable_info.keys():
                _timetable_info[classes[2]] = [timings]
            else:
                _timetable_info[classes[2]].append(timings)
    
    def check_conflicts(_class_info, _cur_timetable):
        for classes in _class_info:
            # Checks if any date conflicts, if no conflicting dates, continue
            if classes[2] in _cur_timetable.keys():
                # Checks if any time conflicts
                for timings in _cur_timetable[classes[2]]:
                    # after class: class start time > timings end time
                    # before class: class end time < timings start time
                    if classes[3][1] < timings[0] or timings[1] < classes[3][0]: 
                        continue 
                    elif all([timings[2], classes[5]]): # Only possible to return false when a remark is empty []
                        if any(week in classes[5] for week in timings[2]): return True # Conflicts found, similar week found!     
                        else: continue # Timing conflicts but the week are different. 
                    else:
                        return True # Conflicts found, due to remarks having special comments ()
        return False
    
    def timetable_parser(_timetable, _course_details):
        def get_class_info(_data:dict, _course_name, _index):
            for _course_info in _data.values():
                if _course_info['Course name'] == _course_name:
                    return _course_info[_index]
            return False
        
        parsed_data = [[[] for _ in range(16)] for _ in range(7)]
        days_arr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        # time_arr = [800, 830, 930, 1030, 1130, 1230, 1330, 1430, 1530, 1630, 1730, 1830, 1930, 2030, 2130, 2230]
        for course, index in _timetable.items():
            course_name = course.split(' ')[0]
            classes = get_class_info(_course_details, course, index)
            for _class in classes: # ['Lec/Studio', 'SCL4', 'Wed', '0930to1120', 'LT19', ''] -> ['CZ2100', 'LEC/STU', '1', 'ONLINE']
                # convert timestamp int:
                timeslot = [int(t) for t in _class[3].split('to')]
                start_time, duration = timeslot[0], (timeslot[1]//100-timeslot[0]//100)
                parsed_data[days_arr.index(_class[2])][(start_time-830)//100 + 1] = [course_name, _class[0], duration, _class[5]]
        return parsed_data

    copy_data = deepcopy(course_data)
    convert_data_details(copy_data)
    
    # Create a dictionary to store the assigned indexes for each course name
    timetable = {}
    timetable_info = {}
    conflict_courses = []
    # Getting the course details by ranking
    for course_details in copy_data.values():
        course_name = course_details['Course name']
        conflict = True
        # Getting the indexes, FCFS
        for index in [k for k in course_details.keys() if k != 'Course name']:
            if not check_conflicts(course_details[index], timetable_info):
                timetable.update({course_name: index})
                insert_timetable(timetable_info, course_details[index])
                conflict = False
                break
        if conflict:
            conflict_courses.append(course_name)
            
    return [conflict_courses, timetable_parser(timetable, course_data), timetable, timetable_info]