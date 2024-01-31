import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fetch_data import FetchData
from utils import *
from tools import *

# from tools.generate_timetable import generate_timetable
# from tools.optimizer import Optimizer

app = FastAPI()
# localdb = Local_DB()
_encryption = Encryption()

# Configure CORS to allow requests from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class TimetableRequest(BaseModel):
    course_lists: str
    topn: int = None
    debugged: bool = False

class ValidateCourses(BaseModel):
    course_lists: str
    
# class Account(BaseModel):
#     access_token: str = None
#     username: str = None
#     password: str = None

# @app.get("/segmentation_analysis")
# async def get_text(input):
#     ...

# @app.post("/validate")
# async def validate(request_data: Account):
#     print("Validate called")
#     return validate_account_info(request_data.username, request_data.password)

# @app.post("/login")
# async def login(request_data: Account):
#     print("Login called")
#     try:
#         assert _encryption.set_key(request_data.access_token)
#         _encryption.encrypt_and_save_data(f"{request_data.username}, {request_data.password}")
#         return True
#     except:
#         return False

@app.post("/validate_courses")
async def validate_courses(request_data: ValidateCourses):
    return get_course_text(request_data.course_lists, get_name=True)
    
@app.post("/get_timetable_plan")
async def get_timetable_plan(request_data: TimetableRequest):
    print("Received:", request_data)
    course_list = get_course_text(request_data.course_lists)
    print("Received:" ,request_data.course_lists, "Parsed valid:", course_list)
    course_data = FetchData().get_courses(course_list)
    print(course_list)
    opt = Optimizer(course_data)
    print("Done 1")
    data = opt.generate_timetable(topn=request_data.topn)
    print("Done 2")
    data.update({"validCourses": course_list})
    print("Done 3")
    return data
    
@app.post("/handle_clean_up")
async def handle_clean_up():
    return _encryption.remove_saved_datas()

# uvicorn main:app --host localhost --port 5000
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)