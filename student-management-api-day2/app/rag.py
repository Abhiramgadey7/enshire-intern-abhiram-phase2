def generate_answer(question: str):

    knowledge = {
        "student": "Students can be created, updated, deleted and searched using this API.",
        "api": "This project uses FastAPI to build REST APIs.",
        "authentication": "JWT authentication is used for securing API endpoints."
    }

    question = question.lower()

    for key, value in knowledge.items():
        if key in question:
            return value

    return "No relevant information found."