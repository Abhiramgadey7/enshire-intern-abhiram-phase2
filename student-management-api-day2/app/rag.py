documents = [
    "Students can create, update, view and delete their records.",
    "Authentication uses JWT tokens for secure access.",
    "Admins have permission to access admin routes.",
    "The API supports student management operations."
]


def generate_answer(question: str):
    question = question.lower()

    for document in documents:
        if any(word in document.lower() for word in question.split()):
            return {
                "question": question,
                "answer": document
            }

    return {
        "question": question,
        "answer": "No relevant information found."
    }