import json
import os

class Local_DB():
    def __init__(self):
        self._cur_path = os.path.dirname(__file__)
        self.database_path = os.path.join(self._cur_path, "database.json")
        self.data = self.__load_db()
        
    def __load_db(self) -> dict:
        with open(self.database_path) as json_file:
            return json.load(json_file)
        
    def query_database(self, courses:list) -> dict:
        return {c:self.data[c] for c in self.data.keys() if c[:6] in courses}, [unknown for unknown in courses if unknown in self.data['Unknown']]
    
    def data_exists(self, data:str|list, match:bool=True) -> bool:
        existing_course_codes = [c[:6] for c in self.data]
        if type(data) == list:
            filtered = [course in existing_course_codes for course in data]
            return all(filtered) if match else any(filtered)
        elif type(data) == str:
            return data in existing_course_codes
    
    def which_data_not_exists(self, data) -> list:
        ram = ''.join(self.data.keys())
        return [course for course in data if course not in ram and course not in self.data['Unknown']]
        
    def peek(self) -> list:
        return [k for k in self.data.keys() if k not in ['TEST']]
        
    def update_db(self, new_data:json, not_found_data:list=[], indentation=2, override=False) -> bool:
        if override: self.data = new_data  
        else: 
            self.data.update(new_data)
            self.data['Unknown']+=not_found_data
        with open(self.database_path, 'w') as outfile:
            json.dump(self.data, outfile, indent=indentation)
        return True
        
    def reset(self) -> bool:
        return self.update_db({'TEST':True, 'Unknown':[]}, override=True)