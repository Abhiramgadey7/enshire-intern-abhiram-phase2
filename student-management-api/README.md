# Student Management API

A simple REST API built using Flask to manage student records.

## Features

- Add Student
- View Students
- JSON Responses

## Endpoints

### GET /

Returns API status.

### GET /students

Returns all students.

### POST /students

Add a new student.

Example:

{
    "name": "Abhiram",
    "email": "abhiram@example.com",
    "course": "Python"
}