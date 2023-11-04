import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fetch_data import get_course_data_from_db
from utils import *
from tools import *
import time
# from tools.generate_timetable import generate_timetable
# from tools.optimizer import Optimizer

app = FastAPI()
localdb = Local_DB()

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
    fernet_key: str = "Public"
    username: str = None
    password: str = None
    topn: int = None
    debugged: bool = False

@app.get("/segmentation_analysis")
async def get_text(input):
    ...

@app.post("/get_timetable_plan")
async def get_timetable_plan(request_data: TimetableRequest):
    print("Received:", request_data)
    # course_lists=['CZ3005','CZ4045','CZ4023','CZ4042','CZ4041']
    course_list = get_course(request_data.course_lists)
    print("Received:" ,request_data.course_lists, "Parsed:",course_list)
    fernet_key = request_data.fernet_key
    course_data = get_course_data_from_db(course_list, localdb, fernet_key=fernet_key , username=request_data.username, password=request_data.password, debugged=request_data.debugged)
    opt = Optimizer(course_data)
    return opt.generate_timetable(topn=request_data.topn)

@app.post("/handle_clean_up")
async def handle_clean_up():
    return Encryption().remove_saved_datas()

@app.get("/test1")
async def test1(check_param, check_param2="b", check_param3=None):
    x = lambda x,y : print(x,y)
    return {"data": None}

@app.get("/test2")
async def test2(check_param = None):
    assert check_param
    course_lists=localdb.peek()[:2]
    course_data = get_course(course_lists, localdb, debugged=True)
    result = generate_timetable(course_data)
    return {"data": result}

# uvicorn main:app --host localhost --port 5000
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)