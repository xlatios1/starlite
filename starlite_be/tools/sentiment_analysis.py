import re
import string

def get_course(search):
    text_without_punctuation = search.translate(str.maketrans(string.punctuation," "*len(string.punctuation)))
    return re.findall('\\b\w{2}\d{4}\\b',text_without_punctuation)