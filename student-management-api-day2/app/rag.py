def generate_answer(question: str):

    knowledge = {
        "student": "Students can be created, updated, deleted and searched using the Student Management API.",
        "api": "This project uses FastAPI to build REST APIs.",
        "authentication": "The API uses JWT authentication for user security."
    }

    question = question.lower()

    for key, value in knowledge.items():
        if key in question:
            return value

    return "No relevant information found."