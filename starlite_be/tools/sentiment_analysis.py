import re
import string
import requests

def get_course_text(search):
    url = 'https://backend.ntusu.org/modsoptimizer/course_code/?search__icontains='
    text_without_punctuation = search.translate(str.maketrans(string.punctuation," "*len(string.punctuation)))
    valid_course = []
    for course in re.findall('\\b\w{2}\d{4}\\b',text_without_punctuation):
        if requests.get(url = url+course).json()['results']:
            if course not in valid_course: valid_course.append(course)
    return valid_course