import json
import os

class Local_DB():
    def __init__(self):
        self._cur_path = os.path.dirname(__file__)
        self.database_path = os.path.join(self._cur_path, "database.json")
        
    def load_db(self) -> dict:
        with open(self.database_path) as json_file:
            return json.load(json_file)
        
    def query_database(self, courses:list, database:dict) -> dict:
        return {c:database[c] for c in courses if c in database.keys()}
    
    def data_exists(self, data:str|list, database:dict, match:bool=True) -> bool:
        if type(data) == type(list):
            filtered = [course in database for course in data]
            return all(filtered) if match else any(filtered)
        elif type(data) == type(str):
            return data in database
    
    def which_data_not_exists(self, data, database) -> list:
        return [course for course in data if course not in database.keys()]
        
    def peek(self, database:dict) -> list:
        return [k for k in database.keys() if k not in ['TEST']]
        
    def write_db(self, data:json, indentation=2) -> bool:
        try:
            with open(self.database_path, 'w') as outfile:
                json.dump(data, outfile, indent=indentation)
            return True
        except:
            return False
        
    def reset(self) -> bool:
        _db_json = self.load_db()
        return self.write_db({k:v for k,v in _db_json.items() if k in ['TEST']})