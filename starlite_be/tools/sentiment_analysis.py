import re
import string
import requests

def get_course_text(search, get_name=False):
    url = 'https://backend.ntusu.org/modsoptimizer/course_code/?search__icontains='
    text_without_punctuation = search.translate(str.maketrans(string.punctuation," "*len(string.punctuation)))
    valid_course = []
    for course in re.findall('\\b\w{6}\\b',text_without_punctuation):
        results = requests.get(url = url+course).json()['results']
        if results:
            if course not in valid_course: 
                if get_name:
                    valid_course.append(results[0])
                else:
                    valid_course.append(course)    
    return valid_course

pass