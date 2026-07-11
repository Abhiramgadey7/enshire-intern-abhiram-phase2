from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
import uuid
from datetime import datetime

app = FastAPI()

# Temporary database
students = []

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())

    logger.info({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3],
        "level": "INFO",
        "message": f"Incoming Request: {request.method} {request.url.path}",
        "request_id": request_id
    })

    response = await call_next(request)

    logger.info({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3],
        "level": "INFO",
        "message": f"Response Status: {response.status_code}",
        "request_id": request_id
    })

    response.headers["X-Request-ID"] = request_id
    return response


# Root endpoint
@app.get("/")
def home():
    return {"message": "Student Management API Running"}


# Student model
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str


# CREATE - Add student
@app.post("/students")
def create_student(student: Student):
    students.append(student)
    return student


# READ - Get all students
@app.get("/students")
def get_students():
    return students


# READ - Get student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student.id == student_id:
            return student

    return {"error": "Student not found"}


# UPDATE - Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == student_id:
            students[index] = updated_student
            return updated_student

    return {"error": "Student not found"}


# DELETE - Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student.id == student_id:
            students.remove(student)
            return {"message": "Student deleted"}

    return {"error": "Student not found"}