from datetime import timedelta

def convert_data_details(course_data):
    """ It alters every timing to [start_second, end_second], and remarks to list of int of wk classes
    
    E.g. Time info:
            | "0830to1030" -> [30600.0, 37800.0]
         Week info(Remarks):
            | "Wk1-10" -> [1,2,3,4,5,6,7,8,9,10]
             | "Wk3,5,7,9,11,13" -> [3,5,7,9,11,13]
            | "" -> [1,2,3,4,5,6,7,8,9,10,11,12,13,14] # assumes full period
    Returns None, it modifies the data directly.
    """
    for rank in course_data.keys():
        for index in [k for k in course_data[rank].keys() if k != 'Course name']:
            for item in course_data[rank][index]:
                item[3] = [timedelta(hours=int(c_time[:2]), minutes=int(c_time[2:])).total_seconds() for c_time in item[3].split("to")]
                if item[5]:
                    if item[5][:2] == "Wk": # Ensure that the remarks are refering to the weeks and not otherwise, empty array
                        week_detail = item[5][2:].split("-")
                        if len(week_detail) > 1: # Refers to "Wk1-10"
                            item[5] = [i for i in range(int(week_detail[0]), int(week_detail[1])+1)]
                        else: # Refers to "Wk3,5,7,9,11,13"
                            item[5] = [int(i) for i in week_detail[0].split(",")]
                    else: # Refers to "This is a special remark"
                        item[5] = []
                else: # Refers to ""
                    item[5] = [i for i in range(15)]
pass