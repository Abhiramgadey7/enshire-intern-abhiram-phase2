from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
import uuid
from datetime import datetime
import traceback
from app.rag import generate_answer
import app.auth as auth
from app.rag import generate_answer

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
from app.rag import generate_answer


# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Management API",
    version="4.0.0"
)


# Include user routes
app.include_router(users.router)


# -----------------------------
# Logging Configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)



# -----------------------------
# Request Logging Middleware
# -----------------------------

@app.middleware("http")
async def request_logger(request: Request, call_next):

    request_id = str(uuid.uuid4())

    start = datetime.now()

    logger.info(
        f"REQUEST START | "
        f"id={request_id} "
        f"{request.method} {request.url.path}"
    )

    try:

        response = await call_next(request)

        duration = (
            datetime.now() - start
        ).total_seconds()


        logger.info(
            f"REQUEST END | "
            f"id={request_id} "
            f"status={response.status_code} "
            f"time={duration}s"
        )


        response.headers["X-Request-ID"] = request_id

        return response


    except Exception as e:

        logger.error(
            f"REQUEST FAILED | "
            f"id={request_id} "
            f"error={str(e)}"
        )

        raise



# -----------------------------
# Global Exception Handler
# -----------------------------

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.error(
        "Unhandled Exception\n"
        + traceback.format_exc()
    )


    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong"
        }
    )



# -----------------------------
# Home Route
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "Student Management API Running",
        "version": "4.0.0"
    }



# -----------------------------
# Create Student
# -----------------------------

@app.post("/students",
response_model=StudentResponse)
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



# -----------------------------
# Get Students
# -----------------------------

@app.get("/students",
response_model=StudentListResponse)
def get_students(
    limit:int=Query(10,ge=1,le=100),
    offset:int=Query(0,ge=0),
    name:str|None=None,
    course:str|None=None,
    sort:str="id",
    db:Session=Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    query=db.query(Student)


    if name:
        query=query.filter(
            Student.name.ilike(f"%{name}%")
        )


    if course:
        query=query.filter(
            Student.course.ilike(f"%{course}%")
        )


    fields={
        "id":Student.id,
        "name":Student.name,
        "age":Student.age,
        "course":Student.course
    }


    reverse=False

    if sort.startswith("-"):
        reverse=True
        sort=sort[1:]


    if sort not in fields:
        raise HTTPException(
            400,
            "Invalid sort field"
        )


    query=query.order_by(
        fields[sort].desc()
        if reverse
        else fields[sort].asc()
    )


    total=query.count()

    students=query.offset(offset)\
                 .limit(limit)\
                 .all()


    return {
        "total":total,
        "page":(offset//limit)+1,
        "limit":limit,
        "items":students
    }



# -----------------------------
# Get Student
# -----------------------------

@app.get("/students/{student_id}",
response_model=StudentResponse)
def get_student(
    student_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    student=db.query(Student)\
             .filter(Student.id==student_id)\
             .first()


    if not student:
        raise HTTPException(
            404,
            "Student not found"
        )


    return student



# -----------------------------
# Update Student
# -----------------------------

@app.put("/students/{student_id}",
response_model=StudentResponse)
def update_student(
    student_id:int,
    student_data:StudentUpdate,
    db:Session=Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    student=db.query(Student)\
             .filter(Student.id==student_id)\
             .first()


    if not student:
        raise HTTPException(
            404,
            "Student not found"
        )


    student.name=student_data.name
    student.age=student_data.age
    student.course=student_data.course


    db.commit()
    db.refresh(student)


    return student



# -----------------------------
# Delete Student
# -----------------------------

@app.delete("/students/{student_id}")
def delete_student(
    student_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    student=db.query(Student)\
             .filter(Student.id==student_id)\
             .first()


    if not student:
        raise HTTPException(
            404,
            "Student not found"
        )


    db.delete(student)
    db.commit()


    return {
        "message":"Student deleted successfully"
    }
@app.post("/ai/query")
def ai_query(question: str):

    answer = generate_answer(question)

    return {
        "question": question,
        "answer": answer
    }