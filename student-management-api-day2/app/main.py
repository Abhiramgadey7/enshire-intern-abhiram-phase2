from fastapi import FastAPI, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
import uuid
from datetime import datetime

from app.database import Base, engine, get_db
from app import users
from app.models import Student
from app.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentListResponse,
)
import app.auth as auth


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Management API",
    version="3.0.0"
)


# Include authentication routes
app.include_router(users.router)


# Logging Setup
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):

    request_id = str(uuid.uuid4())

    logger.info({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": "INFO",
        "message": f"{request.method} {request.url.path}",
        "request_id": request_id
    })

    response = await call_next(request)

    logger.info({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": "INFO",
        "message": f"Status {response.status_code}",
        "request_id": request_id
    })

    response.headers["X-Request-ID"] = request_id

    return response


# Home Route
@app.get("/")
def home():
    return {
        "message": "Student Management API Running",
        "version": "3.0.0"
    }


# Create Student
@app.post("/students", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    new_student = Student(
        name=student.name,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# Get Students
@app.get("/students", response_model=StudentListResponse)
def get_students(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    name: str | None = None,
    course: str | None = None,
    sort: str = "id",
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    query = db.query(Student)

    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))

    if course:
        query = query.filter(Student.course.ilike(f"%{course}%"))

    allowed_fields = {
        "id": Student.id,
        "name": Student.name,
        "age": Student.age,
        "course": Student.course
    }

    reverse = False

    if sort.startswith("-"):
        reverse = True
        sort = sort[1:]

    if sort not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    column = allowed_fields[sort]

    query = query.order_by(
        column.desc() if reverse else column.asc()
    )

    total = query.count()

    students = query.offset(offset).limit(limit).all()

    page = (offset // limit) + 1

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": students
    }


# Get Student By ID
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# Update Student
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = student_data.name
    student.age = student_data.age
    student.course = student_data.course

    db.commit()
    db.refresh(student)

    return student


# Delete Student
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }