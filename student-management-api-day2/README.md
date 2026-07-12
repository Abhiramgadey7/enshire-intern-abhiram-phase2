# Student Management API

A FastAPI-based Student Management API with JWT Authentication, Logging, Testing, Docker support, and a simple AI (RAG) endpoint.

---

## Features

- User Registration
- User Login (JWT Authentication)
- Create Student
- View Students
- Update Student
- Delete Student
- Logging Middleware
- Global Exception Handling
- Configuration using Environment Variables
- Pytest Test Cases
- AI Question Answering (/ai/ask)
- Docker Support

---

## Requirements

- Python 3.13+
- Docker Desktop (optional)

---

## Install

```bash
pip install -r requirements.txt
```

---

## Run Locally

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000/docs

---

## Run with Docker

```bash
docker compose up --build
```

Open:

http://localhost:8000/docs

---

## API Endpoints

### Authentication

POST /register

POST /login

---

### Students

POST /students

GET /students

GET /students/{id}

PUT /students/{id}

DELETE /students/{id}

---

### AI Endpoint

POST /ai/ask

Example Request

```json
{
    "question": "How can I manage student records?"
}
```

Example Response

```json
{
    "question": "how can i manage student records?",
    "answer": "Students can create, update, view and delete their records."
}
```

---

## Run Tests

```bash
pytest
```

Expected Output

```
11 passed
```

---

## Technologies Used

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Pytest
- Docker

---

## Author

Abhiram Gadey